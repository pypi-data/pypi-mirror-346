# stdlib
import datetime
import logging
import random
import re

# third party
import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, RetryError, SSLError
from requests.packages.urllib3.util.retry import Retry
from requests_futures.sessions import FuturesSession
from urllib3.exceptions import MaxRetryError
# nuevo
from curl_cffi.requests import Session
from .headers import HEADERS
from .impersonates import IMPERSONATE

logger = logging.getLogger(__name__)


DEFAULT_TIMEOUT = 5
DEFAULT_SESSION_URL = "https://finance.yahoo.com"
CRUMB_FAILURE = (
    "Failed to obtain crumb.  Ability to retrieve data will be significantly limited."
)


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def safe_get(session, url, max_retries=30, **kwargs):
    for attempt in range(max_retries):
        try:
            return session.get(url, **kwargs)
        except Exception as e:
            if attempt == max_retries - 1:
                raise


def initialize_session(session=None, **kwargs):
    if session is None:
        impersonate = random.choice(IMPERSONATE)
        headers = random.choice(HEADERS)
        session = Session(
            impersonate=impersonate,
            headers=headers,
            timeout=kwargs.get("timeout", 30),
            verify=kwargs.get("verify", True),
            proxies=kwargs.get("proxies", None)
        )
    return session


def setup_session(session, url: str = None):
    url = url or DEFAULT_SESSION_URL
    try:
        response = safe_get(session, url, allow_redirects=True)
    except SSLError:
        counter = 0
        while counter < 5:
            try:
                session.headers = random.choice(HEADERS)
                response = safe_get(session, url, max_retries=1, verify=False)
                break
            except SSLError:
                counter += 1

    if hasattr(response, "result"):  # por si usas FuturesSession en otro contexto
        response = response.result()

    if "consent" in response.url:
        soup = BeautifulSoup(response.content, "html.parser")
        params = {}
        for param in ["csrfToken", "sessionId"]:
            try:
                params[param] = soup.find("input", attrs={"name": param})["value"]
            except Exception as exc:
                logger.critical(f'Failed to find or extract "{param}". Exception={exc}')
                return session

        response = session.post(
            "https://consent.yahoo.com/v2/collectConsent",
            data={
                "agree": ["agree", "agree"],
                "consentUUID": "default",
                "sessionId": params["sessionId"],
                "csrfToken": params["csrfToken"],
                "originalDoneUrl": url,
                "namespace": "yahoo",
            },
        )

    return session


def get_crumb(session):
    try:
        response = safe_get(session, "https://query2.finance.yahoo.com/v1/test/getcrumb")
    except (ConnectionError, RetryError, Exception):
        logger.critical(CRUMB_FAILURE)
        return None

    if hasattr(session, "result"):  # por compatibilidad
        crumb = response.result().text
    else:
        crumb = response.text

    if not crumb or "<html>" in crumb:
        logger.critical(CRUMB_FAILURE)
        return None

    return crumb


def flatten_list(ls):
    return [item for sublist in ls for item in sublist]


def convert_to_list(symbols, comma_split=False):
    if isinstance(symbols, str):
        if comma_split:
            return [x.strip() for x in symbols.split(",")]
        else:
            return re.findall(r"[\w\-.=^&]+", symbols)
    return symbols


def convert_to_timestamp(date=None, start=True):
    if date is not None:
        return int(pd.Timestamp(date).timestamp())
    if start:
        return int(pd.Timestamp("1942-01-01").timestamp())
    return int(pd.Timestamp.now().timestamp())


def _get_daily_index(data, index_utc, adj_timezone):
    # evalute if last indice represents a live interval
    timestamp = data["meta"]["regularMarketTime"]
    if timestamp is None:
        # without last trade data unable to ascertain if there's a live indice
        has_live_indice = False
    else:
        last_trade = pd.Timestamp.fromtimestamp(timestamp, tz="UTC")
        has_live_indice = index_utc[-1] >= last_trade - pd.Timedelta(2, "S")
    if has_live_indice:
        # remove it
        live_indice = index_utc[-1]
        index_utc = index_utc[:-1]
        ONE_DAY = datetime.timedelta(1)
        # evaluate if it should be put back later. If the close price for
        # the day is already included in the data, i.e. if the live indice
        # is simply duplicating data represented in the prior row, then the
        # following will evaluate to False (as live_indice will now be
        # within one day of the prior indice)
        keep_live_indice = index_utc.empty or live_indice > index_utc[-1] + ONE_DAY

    tz = data["meta"]["exchangeTimezoneName"]
    index_local = index_utc.tz_convert(tz)
    times = index_local.time

    bv = times <= datetime.time(14)
    if (bv).all() or data["meta"].get("exchangeName", "Nope") == "SAO":  # see issue 163
        index = index_local.floor("d", ambiguous=True)
    elif (~bv).all():
        index = index_local.ceil("d", ambiguous=True)
    else:
        # mix of open times pre and post 14:00.
        index1 = index_local[bv].floor("d", ambiguous=True)
        index2 = index_local[~bv].ceil("d", ambiguous=True)
        index = index1.union(index2)

    index = pd.Index(index.date)
    if has_live_indice and keep_live_indice:
        live_indice = live_indice.astimezone(tz) if adj_timezone else live_indice
        if not index.empty:
            index = index.insert(len(index), live_indice.to_pydatetime())
        else:
            index = pd.Index([live_indice.to_pydatetime()], dtype="object")
    return index


def _event_as_srs(event_data, event):
    index = pd.Index([int(v) for v in event_data.keys()], dtype="int64")
    if event == "dividends":
        values = [d["amount"] for d in event_data.values()]
    else:
        values = [
            d["numerator"] / d["denominator"] if d["denominator"] else float("inf")
            for d in event_data.values()
        ]
    return pd.Series(values, index=index)


def _history_dataframe(data, daily, adj_timezone=True):
    data_dict = data["indicators"]["quote"][0].copy()
    cols = [
        col for col in ("open", "high", "low", "close", "volume") if col in data_dict
    ]
    if "adjclose" in data["indicators"]:
        data_dict["adjclose"] = data["indicators"]["adjclose"][0]["adjclose"]
        cols.append("adjclose")

    if "events" in data:
        for event, event_data in data["events"].items():
            if event not in ("dividends", "splits"):
                continue
            data_dict[event] = _event_as_srs(event_data, event)
            cols.append(event)

    df = pd.DataFrame(data_dict, index=data["timestamp"])  # align all on timestamps
    df.dropna(how="all", inplace=True)
    df = df[cols]  # determine column order

    index = pd.to_datetime(df.index, unit="s", utc=True)
    if daily and not df.empty:
        index = _get_daily_index(data, index, adj_timezone)
        if len(index) == len(df) - 1:
            # a live_indice was removed
            df = df.iloc[:-1]
    elif adj_timezone:
        tz = data["meta"]["exchangeTimezoneName"]
        index = index.tz_convert(tz)

    df.index = index
    return df
