"""Home page.

`Home.py` must be in the root directory of the application.
"""

from deps.page_config import PageConfig

# Must be at top of page: https://github.com/xcollantes/stock-analysis-frontend/issues/29
PageConfig(layout="centered").get_config()

import logging
import os

import streamlit as st


from passphrase.utils import is_auth


url_args = st.experimental_get_query_params()


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
