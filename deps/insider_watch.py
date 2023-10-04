"""Calls to get data for insider trading."""

from datetime import date, timedelta
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


@st.cache_data(show_spinner="Querying insider House of Reps trading ...")
def show_house_trades_dataframe(symbol: str) -> None:
    """Use API for Representatives who trade stock in given time.

    Use https://housestockwatcher.com for House of Representatives who
    trade a symbol.
    """
    if not symbol:
        st.write()

    st.write("### US House of Representatives trades")

    symbol: str = symbol.upper()
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

        with st.expander("Data explanation"):
            st.write(
                """Trades of more than $1,000 USD by members of the House must
                be reported either 30 days before the actual trade transaction
                or with a deadline of 45 days after the trade occurs, whichever
                is earlier. 45 days after the trade would cover automated trades
                such as Limit Orders."""
            )
            st.write(
                """_\"Title I of the Ethics in Government Act of
                1978, as amended (5 U.S.C. §§ 13101-13111) (EIGA) requires
                Members, officers, certain employees of the U.S. House of
                Representatives and related offices, and candidates for the
                House of Representatives to file Financial Disclosure (FD)
                Statements with the Clerk of the House of Representatives. In
                addition, the Representative Louise McIntosh Slaughter Stop
                Trading on Congressional Knowledge Act (STOCK Act) amended the
                EIGA to add a requirement for Members, officers, and certain
                employees of the House to report certain securities transactions
                over $1,000 by the earlier of these two dates: (a) 30 days from
                being made aware of the transaction or (b) 45 days from the
                transaction\"_ (Financial Disclosure Statements, [page
                1](https://ethics.house.gov/sites/ethics.house.gov/files/documentsUpdated%20Final%20Combined%202023%20Instruction%20Guide.pdf))."""
            )
            st.write(
                "_More info on US House Financial Disclosure: [ethics.house.gov](https://ethics.house.gov/financial-dislosure/specific-disclosure-requirements)._"
            )
            st.write(
                "_Data source: [housestockwatcher.com](https://housestockwatcher.com)._"
            )


@st.cache_data(show_spinner="Querying insider Senate trading ...")
def show_senate_trades_dataframe(symbol: str) -> None:
    """Use API for Senators who trade stock in a given times.

    Use https://senatestockwatcher.com for Senators who
    trade a symbol.
    """
    if not symbol:
        st.write()

    st.write("### US Senate trades")

    symbol: str = symbol.upper()
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

        with st.expander("Data explanation"):
            st.write(
                """Trades of more than $1,000 USD by members of the House must
                be reported either 30 days before the actual trade transaction
                or with a deadline of 45 days after the trade occurs, whichever
                is earlier. 45 days after the trade would cover automated trades
                such as Limit Orders."""
            )
            st.write(
                """_\"Periodic Transaction Reports (PTRs): Must be filed no
                later than 30 days after receiving written notification that a
                transaction has occurred, but in no case later than 45 days
                after the transaction date. For further information regarding
                PTR requirements, see p. 30, infra.\"_ (Financial Disclosure
                Instructions, [page
                6](https://www.ethics.senate.gov/public/_cache/files/02ccce18-df8d-48cb-bea4-ed14b155cba6/2023-financial-disclosure-report-booklet-for-cy2022.pdf))."""
            )
            st.write(
                "_More info on US Senate Financial Disclosure: [ethics.senate.gov](https://www.ethics.senate.gov/public/index.cfm/financialdisclosure)._"
            )

            st.write(
                "_Data source: [senatestockwatcher.com](https://senatestockwatcher.com)._"
            )


def _show_no_trades(message: str = "No recent trades found"):
    """Write out to Streamlit if no trades or error.

    Args:
        message: Custom message text to output on UI.
    """
    if message:
        st.write(message)
