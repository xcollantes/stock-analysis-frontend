"""Component DataFrames of largest drops."""


import pandas as pd
import streamlit as st

from deps.fmp import get_top_losing
from deps.github import get_static_company_data


class TopDrops:
    def __init__(
        self,
        drop_percent: float,
        security_type: str = "stock",
        sector: str = "Technology",
        industry: str = "",
    ) -> None:
        """Initiate instance.

        Args:
            drop_percent: Threshold for showing percent decrease for the day.
            security_type: 'stock', 'etf', 'trust'
            sector: 'Basic Materials', 'Communication Services', 'Consumer
                Cyclical'...
            industry: 'Aerospace & Defense', 'Agricultural Inputs','Auto &
                Truck', 'Dealerships'...
        """
        self.drop_percent = drop_percent
        self.security_type = security_type
        self.sector = sector
        self.industry = industry

    def _create_drop_dataframe(self) -> pd.DataFrame:
        """Join drops DataFrame with company data."""

        # Top drops for the day
        top_losses_df: pd.DataFrame = get_top_losing(self.drop_percent)
        top_losses_df = top_losses_df.sort_values(
            by=["changesPercentage"], ascending=True, ignore_index=True
        )

    def _format_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add styling to DataFrame."""
        return (
            df.style.format(
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

    def _filter_drops(self) -> pd.DataFrame:
        """Filter by sector. Filter here to reduce calls to APIs."""
        top_loss_static_df: pd.DataFrame = top_loss_static_df[
            (top_loss_static_df["Type"] == self.industry)
            & (top_loss_static_df["Sector"] == self.sector)
        ].reset_index(drop=True)

    # Append data from Yahoo Finance
    # yahoo_intermediary_df = pd.DataFrame(
    #     {"MarketCap": [], "Volume": [], "52WeekLow": [], "52WeekHigh": []}
    # )

    for symbol in top_loss_static_df["symbol"]:
        info = get_yahoo_metrics(symbol)
        top_loss_static_df.join(info, on=["symbol"])

        # yahoo_intermediary_df.loc[len(yahoo_intermediary_df)] = [
        #     info[0],
        #     info[1],
        #     info[2],
        #     info[3],
        # ]

    # top_loss_static_yahoo_df: pd.DataFrame = pd.concat(
    #     [top_loss_static_df, yahoo_intermediary_df], axis=1
    # )

    top_loss_static_yahoo_df

    # Create copy because .rename(columns={"symbol": "Symbol"}) causes KeyError
    # in previous DataFrames
    top_loss_static_yahoo_df.rename(columns={"symbol": "Symbol"}, inplace=True)

    show_drops_df: pd.DataFrame = top_loss_static_yahoo_df[
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

    st.data_editor(
        show_drops_df,
        column_config={
            "ClosingPrice": st.column_config.ProgressColumn(
                "ClosingPrice",
                format="$%.2f",
                min_value=show_drops_df["52WeekLow"].min(),
                max_value=show_drops_df["52WeekHigh"].max(),
            )
        },
    )
