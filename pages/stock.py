"""Individual stock dashboard."""

import os
import logging
import re
import streamlit as st
from deps.charts import show_historical_chart
from deps.page_config import PageConfig

logging.basicConfig(level=logging.INFO, format="%(message)s")

PageConfig(report_bug_link="https://google.com/search?q=help").get_config()
# url_args = st.experimental_get_query_params()


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

        days: int = 5
        selection = selection_days.split(" ")
        if selection[1].startswith("day"):
            days = int(selection[0])
        if selection[1].startswith("month"):
            days = int(selection[0]) * 30
        if selection[1].startswith("year"):
            days = int(selection[0]) * 365

        submit = st.form_submit_button(label="Go")
        if submit:
            if error_message:
                st.error(error_message)
            else:
                show_historical_chart(symbol_value.upper(), days)


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
    main()
