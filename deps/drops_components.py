"""Component DataFrames of largest drops."""


import pandas as pd
from deps.yahoo import get_yahoo_overview_company_metrics
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

    def get_drop_dataframe(self) -> pd.DataFrame:
        """Return largest drops of the day in DataFrame stylized."""
        return self._format_drop_dataframe(self._create_drop_dataframe())

    def _create_drop_dataframe(self) -> pd.DataFrame:
        """Join drops DataFrame with company data."""

        # Top drops for the day
        top_losses_df: pd.DataFrame = get_top_losing(self.drop_percent)
        static_co_df: pd.DataFrame = get_static_company_data()

        top_losses_df = (
            top_losses_df.merge(
                static_co_df,
                how="left",
                on=["symbol"],
            )
            .rename(columns={"name_x": "name"})
            .drop(labels=["name_y"], axis=1)  # Remove duplicate column from merge
        )

        if self.sector:
            top_losses_df = top_losses_df[top_losses_df["sector"] == self.sector]

        if self.industry:
            top_losses_df = top_losses_df[top_losses_df["industry"] == self.industry]

        if self.sector or self.industry:
            top_losses_df = top_losses_df.reset_index(drop=True)

        # Append data from Yahoo Finance
        #
        # Use intermediary DataFrame and concat. This is faster than joining
        # onto the `top_losses_df` DataFrame.
        yahoo_intermediary_df = pd.DataFrame(
            {"marketCap": [], "volume": [], "52WeekLow": [], "52WeekHigh": []}
        )

        for symbol in top_losses_df["symbol"]:
            overview_info_df: pd.DataFrame = get_yahoo_overview_company_metrics(symbol)
            yahoo_intermediary_df.loc[len(yahoo_intermediary_df)] = [
                overview_info_df[0],
                overview_info_df[1],
                overview_info_df[2],
                overview_info_df[3],
            ]

        top_losses_df = pd.concat([top_losses_df, yahoo_intermediary_df], axis=1)

        top_losses_df = top_losses_df.sort_values(
            by=["changesPercentage"], ascending=True, ignore_index=True
        )

        return top_losses_df

    def _format_drop_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
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
