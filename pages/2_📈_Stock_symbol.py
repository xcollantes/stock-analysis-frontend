"""Individual stock dashboard."""


from deps.page_config import PageConfig

# Must be at top of page: https://github.com/xcollantes/stock-analysis-frontend/issues/29
PageConfig().get_config()

import os
import logging
import streamlit as st
from deps.common.errors import symbol_has_error
from deps.charts.charts import (
    days_ago_input,
    show_financial_metrics_competitors_chart,
    show_historical_chart,
)
from deps.insider_watch import show_house_trades_dataframe, show_senate_trades_dataframe
from passphrase.utils import is_auth
from deps.news_deps.news_render import show_news

logging.basicConfig(level=logging.INFO, format="%(message)s")

url_args = st.experimental_get_query_params()


def main() -> None:
    with st.form(key="stock_info_form"):
        symbol_value = st.text_input(
            label="Stock symbol", max_chars=10, placeholder="GOOG"
        ).strip()
        error_message: str = symbol_has_error(symbol_value)

        selection_days: str = st.selectbox(
            "Days ago price history",
            ("5 days", "30 days", "60 days", "90 days", "6 months", "1 year"),
            index=5,  # Default selection on render
        )

        submit = st.form_submit_button(label="Go")

    if submit:
        if error_message:
            st.error(error_message)
        else:
            show_historical_chart(symbol_value.upper(), days_ago_input(selection_days))
            st.write()
            st.write("### Competitor benchmarks")
            st.write(
                "If a company fundamentals outperform competitors, this would be a signal of an opportunity."
            )
            show_financial_metrics_competitors_chart(symbol_value)
            show_house_trades_dataframe(symbol_value)
            show_senate_trades_dataframe(symbol_value)


if __name__ == "__main__":
    logging.info("%s running", os.path.basename(__file__))
    is_auth(main, url_args)
