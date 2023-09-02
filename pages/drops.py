"""Find top drops."""

import logging

from deps.drops_components import TopDrops
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
    st.dataframe(drops.get_drop_dataframe())

    # selection = False
    # if selection:
    #     show_historical_chart("GOOG", 10)


if __name__ == "__main__":
    logging.info("Running")
    is_auth(main, url_args)
