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

    ticker_scores_df: pd.DataFrame = news_data_df[
        [
            "url",
            "ticker_sentiment.ticker",
            "ticker_sentiment.relevance_score",
            "ticker_sentiment.ticker_sentiment_score",
        ]
    ]

    ticker_scores_df["weighted_score"] = (
        ticker_scores_df["ticker_sentiment.relevance_score"]
        * ticker_scores_df["ticker_sentiment.ticker_sentiment_score"]
    )

    weighted_sentiment_avg: float = (
        ticker_scores_df["weighted_score"].sum()
        / ticker_scores_df["ticker_sentiment.relevance_score"].sum()
    )

    st.write(f"{symbol.upper()} sentiment score of top 1,000 news recent articles.")

    st.write(round(weighted_sentiment_avg, 4))

    with st.expander("Data explanation"):
        st.write(
            f"{symbol.upper()} sentiment score of top 1,000 news recent articles. "
            + "Sentiment scores are weighted with article relevance."
        )
        st.write(
            "Data source, https://www.alphavantage.co, computes the relevance and sentiment for each article."
        )
        st.write(
            "One article has many symbols; for example, an article 'Tech stocks rise' may have multiple symbols such as GOOGL, META, AMZN. Each symbol is assigned relevance and sentiment scores."
        )
        st.write(
            "A weighted average is taken of symbol sentiments for calculating overall market news sentiment."
        )
        st.latex("{Weighted Mean} = {\sum_{i=1}^{n} w_i \cdot x_i}{\sum_{i=1}^{n} w_i}")

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


def show_sentiment_from_news(symbol: str):
    """Sentiment score from news articles."""
