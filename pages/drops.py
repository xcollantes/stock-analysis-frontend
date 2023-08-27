"""Find top drops."""

import logging

import pandas as pd
import streamlit as st
from deps.fmp import get_top_losing

from deps.github import get_static_company_data
from deps.page_config import PageConfig
from deps.yahoo import (
    get_yahoo_metrics,
)
from deps.charts import show_historical_chart
from passphrase.utils import is_auth

logging.basicConfig(level=logging.INFO, format="%(message)s")
url_args = st.experimental_get_query_params()

PageConfig().get_config()


def main() -> None:
    st.title("Top drops")
    st.write(
        "Find the largest shocks of the day in a market may lead to finding an undervalued stock."
    )

    # 'stock', 'etf', 'trust'
    SECURITY_TYPE: str = "stock"

    # 'Basic Materials', 'Communication Services', 'Consumer Cyclical'...
    SECTOR: str = "Technology"

    # 'Aerospace & Defense', 'Agricultural Inputs', 'Auto & Truck
    # Dealerships'...
    INDUSTRY: str = ""

    # Top drops for the day
    top_losses_df: pd.DataFrame = get_top_losing(0.10)
    top_losses_df = top_losses_df.sort_values(
        by=["changesPercentage"], ascending=True, ignore_index=True
    )

    # Merge with static set containing company data
    static_co_df: pd.DataFrame = get_static_company_data()
    top_loss_static_df: pd.DataFrame = top_losses_df.merge(
        static_co_df[
            [
                "symbol",
                "exchange",
                "exchangeShortName",
                "type",
                "sector",
                "industry",
                "description",
                "website",
            ]
        ],
        how="left",
        on="symbol",
    )

    # Rename fields to match appended data later
    top_loss_static_df: pd.DataFrame = top_loss_static_df.rename(
        columns={
            # "symbol": "Symbol",  # Causes KeyError
            "name": "Name",
            "change": "DayChange",
            "price": "ClosingPrice",
            "changesPercentage": "PercentDayChange",
            "exchange": "Exchange",
            "exchangeShortName": "ExchangeShortName",
            "sector": "Sector",
            "industry": "Industry",
            "description": "Description",
            "type": "Type",
            "website": "Website",
        }
    )

    # Filter by sector. Filter here to reduce calls to APIs.
    top_loss_static_df: pd.DataFrame = top_loss_static_df[
        (top_loss_static_df["Type"] == SECURITY_TYPE)
        & (top_loss_static_df["Sector"] == SECTOR)
    ].reset_index(drop=True)

    # Append data from Yahoo Finance
    yahoo_intermediary_df = pd.DataFrame(
        {"MarketCap": [], "Volume": [], "52WeekLow": [], "52WeekHigh": []}
    )

    for symbol in top_loss_static_df["symbol"]:
        info = get_yahoo_metrics(symbol)
        yahoo_intermediary_df.loc[len(yahoo_intermediary_df)] = [
            info[0],
            info[1],
            info[2],
            info[3],
        ]

    top_loss_static_yahoo: pd.DataFrame = pd.concat(
        [top_loss_static_df, yahoo_intermediary_df], axis=1
    )

    # Create copy because .rename(columns={"symbol": "Symbol"}) causes KeyError
    # in previous DataFrames
    top_loss_static_yahoo.rename(columns={"symbol": "Symbol"}, inplace=True)

    show_drops_df: pd.DataFrame = top_loss_static_yahoo[
        [
            "Symbol",
            "Name",
            "PercentDayChange",
            "52WeekLow",
            "ClosingPrice",
            "52WeekHigh",
            "MarketCap",
            "Volume",
            "Sector",
            "Industry",
            "Type",
            "Exchange",
        ]
    ]

    # Show DataFrame with ranked top loss
    st.dataframe(
        show_drops_df.style.format(
            formatter={
                "PercentDayChange": "{:.1f}%",
                "52WeekLow": "${:.2f}",
                "ClosingPrice": "${:.2f}",
                "52WeekHigh": "${:.2f}",
                "MarketCap": "${:,.2f}",
                "Volume": "{:,.0f}",
            }
        )
        .background_gradient(subset=["PercentDayChange"], cmap="autumn")
        .background_gradient(subset=["MarketCap"], cmap="Greens")
        .highlight_null(color="gray")
    )

    selection = False
    if selection:
        show_historical_chart("GOOG", 10)


if __name__ == "__main__":
    logging.info("Running")
    is_auth(main, url_args)
