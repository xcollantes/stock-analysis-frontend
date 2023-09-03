"""Individual stock dashboard."""

import os
import logging
import re
import streamlit as st
from deps.charts import days_ago_input, show_historical_chart
from deps.page_config import PageConfig
from passphrase.utils import is_auth

logging.basicConfig(level=logging.INFO, format="%(message)s")

url_args = st.experimental_get_query_params()

PageConfig().get_config()


def main() -> None:
    with st.form(key="stock_info_form"):
        symbol_value = st.text_input(
            label="Stock symbol", max_chars=10, placeholder="GOOG"
        ).strip()
        error_message: str = symbol_has_error(symbol_value)

        selection_days: str = st.selectbox(
            "Days ago price history",
            ("5 days", "30 days", "60 days", "90 days", "6 months", "1 year"),
        )

        submit = st.form_submit_button(label="Go")
        if submit:
            if error_message:
                st.error(error_message)
            else:
                show_historical_chart(
                    symbol_value.upper(), days_ago_input(selection_days)
                )


def symbol_has_error(symbol_query: str) -> str:
    """Check stock query is valid, if not returns error message."""
    if symbol_query == "":
        return "Enter stock symbol"
    if not bool(re.match("^[a-zA-Z]+$", symbol_query)):
        return "Letters only"
    if not len(symbol_query) <= 5:
        return "More than 4 characters"

    return ""


if __name__ == "__main__":
    logging.info("%s running", os.path.basename(__file__))
    is_auth(main, url_args)
