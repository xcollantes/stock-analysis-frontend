"""Calls to get data for insider trading."""

from datetime import date, timedelta
from os import error
import pandas as pd
import requests
import streamlit as st


@st.cache_data(show_spinner="Querying House transactions ...")
def _get_ticker_transactions_house(symbol: str) -> pd.DataFrame:
    """Get House Watcher data for all symbols."""
    symbol: str = symbol.upper()

    house_response = requests.get(
        "https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json",
        timeout=5,
    )

    return pd.json_normalize(house_response.json())


@st.cache_data(show_spinner="Querying Senate transactions ...")
def _get_ticker_transactions_senate(symbol: str) -> pd.DataFrame:
    """Get Senate Watcher data for all symbols."""
    symbol: str = symbol.upper()
    senate_response = requests.get(
        "https://senate-stock-watcher-data.s3-us-west-2.amazonaws.com/aggregate/all_ticker_transactions.json",
        timeout=5,
    )

    return pd.json_normalize(senate_response.json())


# @st.cache_data(show_spinner="Querying insider House of Reps trading ...")
def show_house_trades_dataframe(symbol: str) -> None:
    """Use API for Representatives who trade stock in given time.

    Use https://housestockwatcher.com for House of Representatives who
    trade a symbol.
    """
    if not symbol:
        st.write()

    df = _get_ticker_transactions_house(symbol)

    stock_df: pd.DataFrame = df[df["ticker"] == symbol].reset_index(drop=True)

    if stock_df.empty:
        _show_no_trades()
    else:
        stock_df["transaction_date"] = pd.to_datetime(
            stock_df["transaction_date"], format="%Y-%m-%d", errors="coerce"
        )

        # Using last 2 years
        # Members are required to file 60 days
        # https://ethics.house.gov/financial-dislosure/specific-disclosure-requirements
        stock_df = stock_df[
            stock_df["transaction_date"].dt.date > date.today() - timedelta(days=600)
        ]

        if stock_df.empty:
            _show_no_trades()
        else:
            st.write("### US House of Representatives trades")
            st.write(
                "See [ethics.house.gov](https://ethics.house.gov/financial-dislosure/specific-disclosure-requirements) for requirements on government filing."
            )
            st.dataframe(
                stock_df.sort_values(by="transaction_date", ascending=False)[
                    [
                        "disclosure_date",
                        "transaction_date",
                        "owner",
                        "representative",
                        "district",
                        "state",
                        "asset_description",
                        "type",
                        "amount",
                        "party",
                        "sector",
                    ]
                ].reset_index(drop=True)
            )


@st.cache_data(show_spinner="Querying insider Senate trading ...")
def show_senate_trades_dataframe(symbol: str) -> None:
    """Use API for Senators who trade stock in a given times.

    Use https://senatestockwatcher.com for Senators who
    trade a symbol.
    """
    if not symbol:
        st.write()

    df = _get_ticker_transactions_senate(symbol)

    stock_df: pd.DataFrame = df[df["ticker"] == symbol].reset_index(drop=True)

    if stock_df.empty:
        _show_no_trades()
    else:
        stock_trades_df = pd.json_normalize(
            stock_df.transactions.iloc[0]
        )  # Only one row per stock

        stock_trades_df["transaction_date"] = pd.to_datetime(
            stock_trades_df["transaction_date"]
        )

        # Last 2 years
        stock_trades_df = stock_trades_df[
            stock_trades_df["transaction_date"].dt.date
            > date.today() - timedelta(days=600)
        ]

        if stock_trades_df.empty:
            _show_no_trades()
        else:
            st.write("### US Senate trades")
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
                ].reset_index(drop=True)
            )


def _show_no_trades(message: str = "No recent trades"):
    """Write out to Streamlit if no trades or error.

    Args:
        message: Custom message text to output on UI.
    """
    st.write("### Last 6 months trades by United States House of Reps")
    if message:
        st.write(message)
