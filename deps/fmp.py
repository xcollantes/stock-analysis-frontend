"""API calls to FinancialModelPrep.com API."""


import logging
import pandas as pd
import streamlit as st
import requests

FMG_KEY: str = st.secrets.financial_model_prep.apikey


def get_earnings_surprises_fmp(symbol: str) -> pd.DataFrame:
    """Return DataFrame with expected and actual earnings results."""
    url = f"https://financialmodelingprep.com/api/v3/earnings-surprises/{symbol}?apikey={apikey}"
    response = requests.Response = requests.get(
        url, timeout=st.secrets.api_config.timeout_seconds
    )
    return pd.json_normalize(response.json())


@st.cache_data
def get_top_losing(percent_threshold: float) -> pd.DataFrame:
    """Return stocks with largest drops from open to close price.

    Args:
        percent_threshold: Percent drop or greater to filter symbols.

    Returns:
        DataFrame of symbol, name, change, price, changesPercentage, exchange,
        exchangeShortName.
    """
    logging.info("API call: top drops")
    response: requests.Response = requests.get(
        "https://financialmodelingprep.com/api/v3/stock_market/losers?"
        + f"apikey={FMG_KEY}",
        timeout=st.secrets.api_config.timeout_seconds,
    )
    response_df = pd.json_normalize(response.json())
    return response_df[response_df["changesPercentage"] < percent_threshold * -100]
