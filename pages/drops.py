"""Find top drops."""

import logging

import pandas as pd
import streamlit as st
from deps.fmp import get_top_losing

from deps.github import get_static_company_data
from deps.page_config import PageConfig
from deps.yahoo import (
    get_company_yahoo,
    get_yahoo_metrics,
)
from passphrase.utils import is_auth

logging.basicConfig(level=logging.INFO, format="%(message)s")
url_args = st.experimental_get_query_params()

PageConfig().get_config()


def main() -> None:
    st.title("Top drops")
    st.write(
        "Find the largest shocks of the day in a market may lead to finding an undervalued stock."
    )

    # selection = False
    # if selection:
    #     show_historical_chart("GOOG", 10)


if __name__ == "__main__":
    logging.info("Running")
    is_auth(main, url_args)
