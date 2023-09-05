"""Find top drops."""

import logging
from deps.charts import (
    days_ago_input,
    show_financial_metrics_competitors_chart,
    show_historical_chart,
)

from deps.drops_components import TopDrops
from pages.stock import symbol_has_error
import streamlit as st

from deps.page_config import PageConfig
from passphrase.utils import is_auth

logging.basicConfig(level=logging.INFO, format="%(message)s")
url_args = st.experimental_get_query_params()

PageConfig().get_config()


def main() -> None:
    st.title("Top drops")
    st.write(
        "Find the largest shocks of the day in a market may lead to finding an undervalued stock."
    )

    drops = TopDrops(0.10)
    drops.get_drop_table(color="purple")

    with st.form(key="stock_drop_form"):
        symbol_value = st.text_input(
            label="Stock symbol",
            max_chars=10,
        ).strip()
        error_message: str = symbol_has_error(symbol_value)

        submit = st.form_submit_button(label="Go")
        if submit:
            if error_message:
                st.error(error_message)
            else:
                show_historical_chart(symbol_value, days_ago_input("6 months"))
                st.write("### Competitor benchmarks")
                show_financial_metrics_competitors_chart(symbol_value)


if __name__ == "__main__":
    logging.info("Running")
    is_auth(main, url_args)
