# stdlib
import os

# third party
import pandas as pd

from .utils import get_crumb, initialize_session, setup_session
from .utils.countries import COUNTRIES

BASE_URL = "https://query2.finance.yahoo.com"


def _make_request(
    url: str,
    response_field: str | None = None,
    country: str | None = None,
    method: str = "get",
    params: dict = {},
    data: dict | None = None,
    **kwargs
):
    if country:
        country = country.lower()
        try:
            params.update(COUNTRIES[country])
        except KeyError:
            valid = ", ".join(sorted(COUNTRIES.keys()))
            raise KeyError(f"{country} is not a valid option. Valid options include {valid}")

    setup_url = kwargs.pop("setup_url", os.getenv("YF_SETUP_URL", None))
    session = initialize_session(**kwargs)
    session = setup_session(session, setup_url)
    crumb = get_crumb(session)
    if crumb is not None:
        params["crumb"] = crumb
    r = getattr(session, method)(url, params=params, json=data)
    json_data = r.json()
    if response_field:
        try:
            return json_data[response_field]["result"]
        except (TypeError, KeyError):
            return json_data.get(response_field)
    return json_data


def search(
    query: str,
    country: str = "United States",
    quotes_count: int = 10,
    news_count: int = 10,
    first_quote: bool = False,
):
    """Search Yahoo Finance for anything"""
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    params = {"q": query, "quotes_count": quotes_count, "news_count": news_count}
    data = _make_request(url, country=country, params=params)
    if first_quote:
        return data["quotes"][0] if data.get("quotes") else data
    return data


def get_currencies():
    """Get a list of currencies"""
    url = f"{BASE_URL}/v1/finance/currencies"
    return _make_request(url, response_field="currencies", country="United States")


def get_exchanges():
    """Get a list of available exchanges and their suffixes"""
    url = "https://help.yahoo.com/kb/finance-for-web/SLN2310.html?impressions=true"
    dataframes = pd.read_html(url)
    return dataframes[0]


def get_market_summary(country: str = "United States"):
    """Get a market summary"""
    url = f"{BASE_URL}/v6/finance/quote/marketSummary"
    return _make_request(url, response_field="marketSummaryResponse", country=country)


def get_trending(country: str = "United States"):
    """Get trending stocks for a specific region"""
    try:
        region = COUNTRIES[country.lower()]["region"]
    except KeyError:
        valid = ", ".join(COUNTRIES.keys())
        raise KeyError(f"{country} is not a valid option. Valid options include {valid}")
    url = f"{BASE_URL}/v1/finance/trending/{region}"
    return _make_request(url, response_field="finance", country=country)[0]
