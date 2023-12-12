"""Build news Streamlit features."""

import pandas as pd
import streamlit as st
from deps.news.news_query import get_news_data


def show_news(symbol: str, count: 50 | 1000, height: None | int = None) -> None:
    """Show Streamlit visuals for news articles.

    Args:
        symbol: Stock symbol.
        count: Number of articles to show.
    """
    articles_df, news_data_df = get_news_data(symbol, count)

    st.dataframe(news_data_df)
    st.data_editor(
        articles_df,
        height=height,
        column_config={
            "banner_image": st.column_config.ImageColumn(),
            "url": st.column_config.LinkColumn(
                max_chars=100, validate="^(https?):\/\/"
            ),
        },
        hide_index=True,
    )

    # for idx in range(len(columns)):
    #     article = articles[idx]

    #     columns[idx].write(f"[{article['title']}]({article['url']})")
    #     columns[idx].image(article["banner_image"], caption=article["summary"])


def show_sentiment_from_news(symbol: str):
    """Sentiment score from news articles."""
