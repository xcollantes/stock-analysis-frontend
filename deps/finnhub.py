"""API calls to Finnhub.io API."""

import datetime
import json
import logging
import pandas as pd
import requests
import streamlit as st


FINNHUB_KEY: str = st.secrets.finnhub.apikey


@st.cache_data(show_spinner="Querying company data ...")
def _get_finnhub_company_metrics(symbol: str) -> json:
    """Gets all metrics for company including historical prices."""
    try:
        logging.info("API call: Finnhub.io: Company overall metrics")
        response: requests.Response = requests.get(
            f"https://finnhub.io/api/v1/stock/metric?symbol={symbol}&metric=all&token={FINNHUB_KEY}",
            timeout=st.secrets.api_config.timeout_seconds,
        )
        return response.json()

    except requests.HTTPError as he:
        logging.error("Error: " + he)


@st.cache_data(show_spinner="Query company metrics ...")
def get_finnhub_company_metrics(symbol: str) -> tuple[str, str, str, str]:
    symbol = symbol.upper()

    all_company_metrics = _get_finnhub_company_metrics(symbol)
    metrics = all_company_metrics["metrics"]

    return (
        metrics["marketCapitalization"],
        metrics["3MonthAverageTradingVolume"],
        metrics["52WeekLow"],
        metrics["52WeekHigh"],
    )


@st.cache_data(show_spinner="Querying earnings results ...")
def _get_finnhub_earnings_data(symbol: str) -> pd.DataFrame:
    """Call Finnhub to get last 4 earnings periods."""
    symbol = symbol.upper()
    finnhub_df: pd.DataFrame = pd.read_json(
        f"https://finnhub.io/api/v1/stock/earnings?symbol={symbol}&token={FINNHUB_KEY}"
    )
    return finnhub_df


@st.cache_data(show_spinner="Calculating earnings results ...")
def get_finnhub_earnings_surprises(symbol: str, days_ago: int = 365) -> pd.DataFrame:
    """Return DataFrame with earnings dates and results.

    Also returns next 4 earnings calls. The limit includes the next 4 earnings
    as the latest 4 entries.
    """
    finnhub_df: pd.DataFrame = _get_finnhub_earnings_data(symbol)

    diff_date: datetime = datetime.now() - datetime.timedelta(days=days_ago)
    earliest_earnings_date: str = diff_date.strftime("%Y-%m-%d")

    finnhub_dated_df = finnhub_df[finnhub_df["period"] >= earliest_earnings_date]

    finnhub_dated_df.sort_values(by=["quarter"], ascending=False, inplace=True)
    result_df = finnhub_dated_df[
        ["estimate", "actual", "surprisePercent", "period"]
    ].rename(
        columns={
            "estimate": "EstimatedEarning",
            "actual": "ActualEarning",
            "surprisePercent": "SurprisePercent",
            "period": "Date",
        }
    )

    return result_df.reset_index(drop=True)




@st.cache_data(show_spinner="Querying competitor data ...")
def get_company_competitors(symbol: str) -> pd.Series:
    """Get list of peers of a given company.

    List of competitor symbols include the input company.

    Args:
      symbol: One stock symbol for a company.

    Returns:
      List of competitor company stock symbols in a Series.
    """
    result = None
    try:
        logging.info("API call: Finnhub.io: Company competitors")
        response: requests.Response = requests.get(
            f"https://finnhub.io/api/v1/stock/peers?symbol={symbol}&token={FINNHUB_KEY}",
            timeout=st.secrets.api_config.timeout_seconds,
        )
        result: json = json.loads(response.content)
    except requests.HTTPError as he:
        logging.error("Error: " + he)

    return pd.Series(result)
