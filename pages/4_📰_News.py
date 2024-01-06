"""Page for news on certain symbols."""


# Must be at top of page: https://github.com/xcollantes/stock-analysis-frontend/issues/29
import os
from deps.page_config import PageConfig

PageConfig().get_config()

import logging
from deps.common.errors import symbol_has_error
import streamlit as st

from deps.news_deps.news_render import show_news
from passphrase.utils import is_auth

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

url_args = st.experimental_get_query_params()


def main():
    with st.form(key="news_form"):
        symbol_value = st.text_input(
            label="See news",
            max_chars=10,
        ).strip()
        error_message: str = symbol_has_error(symbol_value)

        submit = st.form_submit_button(label="Go")

    if submit:
        if error_message:
            st.error(error_message)
        else:
            st.header(f"{symbol_value.upper()} in the news")
            show_news(symbol_value, 50, height=1000)


if __name__ == "__main__":
    logging.info("%s running", os.path.basename(__file__))
    is_auth(main, url_args)
