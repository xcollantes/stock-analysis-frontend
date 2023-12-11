"""Process data for news feature about the selected stock."""

import logging
import requests
import streamlit as st

logging.basicConfig(level=logging.INFO, format="%(message)s")


def get_news_data(symbol: str, count: int):
    news_response = _query_stock_news(symbol, count)
    logging.info("FEED: ", news_response)

    for article in news_response["feed"]:
        print(article)
    return news_response["feed"]


def get_news_sentiment(symbol: str):
    """Get sentiment from news articles.

    Data is coupled with the same call as the news articles themselves.
    """

    return _query_stock_news(symbol)


@st.cache_data(show_spinner="Getting news articles...")
def _query_stock_news(symbol: str, count: int):
    """Show news on a selected stock symbol.

    Args:
        symbol: Stock symbol.

    Return:
        Response news data.
    """
    url: str = (
        "https://www.alphavantage.co/query?function=NEWS_SENTIMENT"
        + "&topic=ipo,blockchain,finance,financial_markets,mergers_and_acquisitions,economy_monetary,technology"
        + f"&tickers={symbol}"
        + f"&limit={count}"
        + f"&sort={st.secrets.alphavantage.sort}"
        + f"&apikey={st.secrets.alphavantage.apikey}"
    )
    print(url)

    response: requests.Response = requests.get(url)
    return response.json()
    # return st.components.v1.iframe(
    #     # f"https://news.google.com/search?q=why%20did%20{symbol}%20stock%20drop%20today&hl=en-US&gl=US&ceid=US%3Aen",
    #     "https://www.bing.com/news/search?q=why+did+googl+stock+fall&FORM=HDRSC7",
    #     # "https://www.bloomberg.com/",
    #     width=800,
    #     height=700,
    #     scrolling=True,
    # )
