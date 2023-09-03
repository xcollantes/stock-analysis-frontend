"""Component DataFrames of largest drops."""


import pandas as pd
import streamlit as st
from deps.yahoo import get_yahoo_overview_company_metrics

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

    def get_drop_dataframe_formatted(self) -> pd.DataFrame:
        """Return largest drops of the day in DataFrame."""
        df: pd.DataFrame = self._create_drop_dataframe()

        df = df[
            [
                "symbol",
                "name",
                "changesPercentage",
                "change",
                "52WeekLow",
                "price",
                "52WeekHigh",
                "marketCap",
                "volume",
                "type",
                "sector",
                "industry",
                "website",
            ]
        ]

        # Format columns
        df.columns = [
            "Symbol",
            "Name",
            "PercentDayChange",
            "PriceChange",
            "52WeekLow",
            "ClosingPrice",
            "52WeekHigh",
            "MarketCap",
            "Volume",
            "Type",
            "Sector",
            "Industry",
            "Website",
        ]

        return df

    def get_drop_table(self, color: str) -> None:
        """Apply styles to DataFrame.

        Args:
            color: HTML color name.
        """
        df: pd.DataFrame = self.get_drop_dataframe_formatted()
        df_styler = (
            df.style.format(
                formatter={
                    "PriceChange": "${:.2f}",
                    "PercentDayChange": "{:.1f}%",
                    "52WeekLow": "${:.2f}",
                    "ClosingPrice": "${:.2f}",
                    "52WeekHigh": "${:.2f}",
                    "MarketCap": "${:,.2f}",
                    "Volume": "{:,.0f}",
                },
                hyperlinks="html",
            )
            .set_properties(subset=["ClosingPrice"], **{"text-align": "right"})
            .background_gradient(subset=["PercentDayChange"], cmap="autumn")
            .background_gradient(subset=["MarketCap"], cmap="Greens")
            .highlight_null(color="gray")
        )

        # https://stackoverflow.com/q/77030320/8278075
        for rowIdx, (low, high) in enumerate(zip(df["52WeekLow"], df["52WeekHigh"])):
            df_styler = df_styler.bar(
                subset=pd.IndexSlice[rowIdx, "ClosingPrice"],
                color=color,
                vmin=low,
                vmax=high,
            )

        # Pandas Styler object is HTML and CSS
        st.markdown(df_styler.to_html(escape=False), unsafe_allow_html=True)

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
