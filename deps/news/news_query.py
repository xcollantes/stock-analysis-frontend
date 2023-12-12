"""Process data for news feature about the selected stock."""

import pandas as pd
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

    # Using URL as the common key to merge the 2 DataFrames
    normalized_articles_pd: pd.DataFrame = pd.json_normalize(
        news,
        record_path=["ticker_sentiment"],
        record_prefix="ticker_sentiment.",
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

    normalized_articles_pd = normalized_articles_pd.astype(
        {
            "ticker_sentiment.ticker_sentiment_score": float,
            "ticker_sentiment.relevance_score": float,
            "overall_sentiment_score": float,
        }
    )

    # Datetime does not have Python native datatype, must convert separately
    normalized_articles_pd["time_published"] = pd.to_datetime(
        normalized_articles_pd["time_published"]
    )

    # Filter only relevant articles
    normalized_articles_pd = normalized_articles_pd[
        normalized_articles_pd["ticker_sentiment.relevance_score"]
        > relevance_lower_threshold
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
                "ticker_sentiment.relevance_score",
                "ticker_sentiment.ticker_sentiment_score",
                "url",
            ]
        ]
        .sort_values("ticker_sentiment.relevance_score", ascending=False)
        .drop_duplicates("url")
    )

    return presentable_articles_pd, normalized_articles_pd


@st.cache_data(
    show_spinner="Getting news articles, calculating relevance and sentiment..."
)
def _query_stock_news(symbol: str, count: 50 | 1000) -> dict:
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

    response: requests.Response = requests.get(url)
    return response.json()
