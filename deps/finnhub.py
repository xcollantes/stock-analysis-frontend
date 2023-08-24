"""API calls to Finnhub.io API."""


import json
import logging
import pandas as pd
import requests
import streamlit as st


FINNHUB_KEY: str = st.secrets.finnhub.apikey


@st.cache_data
def get_competitors(symbol: str) -> pd.Series:
    """Get list of peers of a given company.

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
