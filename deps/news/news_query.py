"""Process data for news feature about the selected stock."""

import pandas as pd
import json
import logging
import requests
import streamlit as st

logging.basicConfig(level=logging.INFO, format="%(message)s")


def get_news_data(symbol: str, count: int) -> pd.DataFrame:
    """News sources must be cleaned and turned into DataFrame.

    Data from alphavantage.co contains sentiment and relevance scores per
    article. Only adding the symbol does not guarantee the quality of the
    relevance of the news articles. Filtering must be applied to get articles
    relevant to the symbol.

    Docs: https://www.alphavantage.co/documentation/#news-sentiment

    Args:
        symbol: Stock symbol.
        count: Number of news articles; either 50 or 1000 for datasource.

    Returns:
        Panda Dataframe with news article data.
    """
    relevance_lower_threshold: float = 0.30
    news_response: dict = _query_stock_news(symbol, count)
    news = news_response["feed"]

    articles_pd = pd.DataFrame = pd.json_normalize(
        news,
        record_path=["topics"],
        record_prefix="topics.",
        meta=[
            "title",
            "url",
            "time_published",
            "authors",
            "summary",
            "banner_image",
            "source",
            "category_within_source",
            "source_domain",
            "overall_sentiment_score",
            "overall_sentiment_label",
        ],
    )

    # Using URL as the common key to merge the 2 DataFrames
    sentiment_pd: pd.DataFrame = pd.json_normalize(
        news,
        record_path=["ticker_sentiment"],
        record_prefix="ticker_sentiment.",
        meta=["url"],
    )

    normalized_articles_pd: pd.DataFrame = pd.merge(
        left=articles_pd, right=sentiment_pd, on="url"
    )

    normalized_articles_pd = normalized_articles_pd.astype(
        {
            "ticker_sentiment.ticker_sentiment_score": float,
            "overall_sentiment_score": float,
            "topics.relevance_score": float,
        }
    )

    # Datetime does not have Python native datatype, must convert separately
    normalized_articles_pd["time_published"] = pd.to_datetime(
        normalized_articles_pd["time_published"]
    )

    # Filter only relevant articles
    normalized_articles_pd = normalized_articles_pd[
        normalized_articles_pd["topics.relevance_score"] > relevance_lower_threshold
    ]

    # User facing for Streamlit
    presentable_articles_pd = pd.DataFrame = (
        normalized_articles_pd[
            [
                "banner_image",
                "title",
                "time_published",
                "source",
                "summary",
                "overall_sentiment_label",
                "overall_sentiment_score",
                "url",
                "topics.relevance_score",
            ]
        ]
        .sort_values("topics.relevance_score", ascending=False)
        .drop_duplicates("url")
    )

    return presentable_articles_pd, normalized_articles_pd


def get_news_sentiment(symbol: str):
    """Get sentiment from news articles.

    Data is coupled with the same call as the news articles themselves.
    """

    return _query_stock_news(symbol)


@st.cache_data(show_spinner="Getting news articles...")
def _query_stock_news(symbol: str, count: 50 | 1000):
    """Show news on a selected stock symbol.

    Limit is either 50 or 1000.
    Data from alphavantage.co.
    Docs: https://www.alphavantage.co/documentation/#news-sentiment

    Args:
        symbol: Stock symbol.

    Return:
        Response news data.
    """
    url: str = (
        "https://www.alphavantage.co/query?function=NEWS_SENTIMENT"
        # + "&topic=ipo,blockchain,finance,financial_markets,mergers_and_acquisitions,economy_monetary,technology"
        + f"&tickers={symbol}"
        + f"&limit={count}"
        + f"&apikey={st.secrets.alphavantage.apikey}"
    )

    # with open("test_data.json", "r") as testdata:
    #     response = json.load(testdata)
    response_pd = requests.get(url)
    return response_pd.json()
    # return response.json()

    # return st.components.v1.iframe(
    #     # f"https://news.google.com/search?q=why%20did%20{symbol}%20stock%20drop%20today&hl=en-US&gl=US&ceid=US%3Aen",
    #     "https://www.bing.com/news/search?q=why+did+googl+stock+fall&FORM=HDRSC7",
    #     # "https://www.bloomberg.com/",
    #     width=800,
    #     height=700,
    #     scrolling=True,
    # )
