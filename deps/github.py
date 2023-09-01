"""Get data from GitHub."""

import logging

import streamlit as st
import pandas as pd


@st.cache_data(show_spinner="Getting static data ...")
def get_static_company_data() -> pd.DataFrame:
    """Get stock data."""
    logging.info("API call: us_tickers.csv")
    csv_df: pd.DataFrame = pd.read_csv(
        "https://raw.githubusercontent.com/xcollantes/stock_analysis_dataset/main/us_tickers.csv"
    )

    return csv_df
