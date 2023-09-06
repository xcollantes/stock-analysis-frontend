"""Home page."""

import logging
import os
from st_pages import Page, show_pages

import streamlit as st

from deps.page_config import PageConfig
from passphrase.utils import is_auth


PageConfig(layout="centered").get_config()
url_args = st.experimental_get_query_params()

show_pages(
    [
        Page("Home.py", "Getting started", ":house:"),
        Page("pages/stock.py", "Search symbol", ":mag:"),
        Page("pages/drops.py", "Top drops", ":chart_with_downwards_trend:"),
    ]
)


def main() -> None:
    st.title("Stock analysis tools")
    st.subheader("Created by Xavier Collantes (xaviercollantes.dev)")
    with open("assets/calc-icon.svg", "r") as svg_file:
        st.write(svg_file.read(), unsafe_allow_html=True)
    st.write("## Drops")
    st.write(
        "Find today's biggest market shock drops and evaluate if an opportunity exists."
    )
    st.write("## Stocks")
    st.write("Find information on a specific stock by symbol.")


if __name__ == "__main__":
    logging.info("%s running", os.path.basename(__file__))
    is_auth(main, url_args)
