"""Calls to get data for insider trading."""

from datetime import date, timedelta
import pandas as pd
import requests
import streamlit as st


@st.cache_data(show_spinner="Querying House transactions ...")
def _get_all_ticker_transactions_house(symbol: str) -> pd.DataFrame:
    """Get House Watcher data for all symbols."""
    symbol: str = symbol.upper()
    response = requests.get(
        "https://senate-stock-watcher-data.s3-us-west-2.amazonaws.com/aggregate/all_ticker_transactions.json"
    )
    return pd.json_normalize(response.json())


@st.cache_data(show_spinner="Querying insider trading ...")
def show_congress_dataframe(symbol: str) -> None:
    """Use API for Representatives who trade stock in the 6 months.

    Use https://senatestockwatcher.com for House of Representatives who
    trade a symbol.
    """
    if not symbol:
        st.write()

    df = _get_all_ticker_transactions_house(symbol)

    st.dataframe(df)
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

        # Using 6 months since members are required to file 60 days
        # https://ethics.house.gov/financial-dislosure/specific-disclosure-requirements
        stock_trades_df = stock_trades_df[
            stock_trades_df["transaction_date"].dt.date
            > date.today() - timedelta(days=120)
        ]

        if stock_trades_df.empty:
            _show_no_trades()
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


def _show_no_trades(message: str = "No recent trades"):
    """Write out to Streamlit if no trades or error.

    Args:
        message: Custom message text to output on UI.
    """
    st.write("### Last 6 months trades by United States House of Reps")
    if message:
        st.write(message)
