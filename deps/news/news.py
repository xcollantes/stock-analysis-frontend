"""Build news Streamlit features."""

import streamlit as st
from deps.news.news_query import get_news_data


def show_news(symbol: str, count: int) -> None:
    """Show Streamlit visuals for news articles.

    Args:
        symbol: Stock symbol.
        count: Number of articles to show.
    """
    articles = get_news_data(symbol, count)

    columns = st.columns(count - 1)

    for idx in range(len(columns)):
        article = articles[idx]

        columns[idx].write(f"[{article['title']}]({article['url']})")
        columns[idx].image(article["banner_image"], caption=article["summary"])


def show_sentiment_from_news(symbol: str):
    """Sentiment score from news articles."""
