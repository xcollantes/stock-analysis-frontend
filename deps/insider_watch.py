"""Calls to get data for insider trading."""

from datetime import date, timedelta
import pandas as pd
import requests
import streamlit as st


@st.cache_data(show_spinner="Querying insider trading ...")
def show_congress_dataframe(symbol: str) -> None:
    """Use API for Congressmembers who trade stock in the 6 months."""
    if not symbol:
        st.write()

    symbol = symbol.upper()
    response = requests.get(
        "https://senate-stock-watcher-data.s3-us-west-2.amazonaws.com/aggregate/all_ticker_transactions.json"
    )
    df: pd.DataFrame = pd.json_normalize(response.json())

    stock_df: pd.DataFrame = df[df["ticker"] == symbol].reset_index(drop=True)
    stock_trades_df = pd.json_normalize(
        stock_df.transactions.iloc[0]
    )  # Only one row per stock

    stock_trades_df["transaction_date"] = pd.to_datetime(
        stock_trades_df["transaction_date"]
    )

    # Using 6 months since members are required to file 60 days
    # https://ethics.house.gov/financial-dislosure/specific-disclosure-requirements
    stock_trades_df = stock_trades_df[
        stock_trades_df["transaction_date"].dt.date > date.today() - timedelta(days=120)
    ]

    if stock_trades_df.empty:
        st.write("### Last 6 months trades by United States Congress")
        st.write("No recent trades")
    else:
        st.write(
            "See [ethics.house.gov](https://ethics.house.gov/financial-dislosure/specific-disclosure-requirements) for requirements on government filing."
        )
        st.dataframe(
            stock_trades_df.sort_values(by="transaction_date", ascending=False)[
                [
                    "transaction_date",
                    "owner",
                    "senator",
                    "type",
                    "amount",
                    "party",
                    "sector",
                    "asset_type",
                    "comment",
                ]
            ]
        )
