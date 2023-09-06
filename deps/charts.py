"""Charts."""


import logging
import altair as alt
import pandas as pd
from deps.finnhub import get_company_competitors
import streamlit as st

from deps.chart_components import (
    competitor_ratio_charts,
    earnings_beat_chart,
    stock_chart_trad_mult,
)
from deps.yahoo import (
    get_company_yahoo,
    get_earnings_surprises_yahoo,
    get_historic_prices,
)


def days_ago_input(days_ago_text: str) -> int:
    """Clean and convert human readable days ago into int.

    Args:
        days_ago_text: Human text such as '5 days', '1 month', '1 year'. Can
        also use single letter such as '1 d', '5 m', '12 y'. There must be a
        single space between the quantity and the time amount.

    Returns:
        Integer of days.
    """
    days: int = 0
    selection = days_ago_text.split(" ")
    if selection[1].startswith("d"):
        days = int(selection[0])
    if selection[1].startswith("m"):
        days = int(selection[0]) * 30
    if selection[1].startswith("y"):
        days = int(selection[0]) * 365
    return days


def show_historical_chart(symbol: str, days_ago: int) -> None:
    """Render company historical price charts with earnings results."""
    info_df = get_company_yahoo(symbol)
    historic_prices_df: pd.DataFrame = get_historic_prices(symbol, days_ago)

    # Earnings graph looks awkward where last earnings call was recent and the
    # next earnings call is in ~90 days.  Remove the earnings graph completely
    # if days duration selection is too low.
    earnings_beat_df: pd.DataFrame = get_earnings_surprises_yahoo(
        symbol, days_ago=days_ago, show_next=(True if days_ago >= 60 else False)
    )  # Get last x quarters

    a_row = info_df.loc[0]
    st.header(f"{a_row.get('longName', '')} ({symbol})")
    st.write(
        f"""
**Industry:** {a_row.get('industry', '')}

**Sector:** {a_row.get('sector', '')}

{a_row.get('longBusinessSummary', '')}

**Employees:** {a_row.get('fullTimeEmployees', '')}

{a_row.get('address1', '')} {a_row.get('city', '')}, {a_row.get('state', '')}, {a_row.get('country', '')}

{a_row.get('website', '')}
"""
    )

    st.write(
        alt.layer(
            stock_chart_trad_mult(historic_prices_df),
            earnings_beat_chart(earnings_beat_df, symbol),
        ).resolve_scale(y="independent")
    )


def show_financial_metrics_competitors_chart(symbol: str) -> None:
    """Render graphs of company against competitors.

    Args:
        symbol: Company stock symbol.
    """
    comp_series: pd.Series = get_company_competitors(symbol)

    show_combined_df: pd.DataFrame = pd.DataFrame()
    desired_columns_show_combined = [
        "symbol",
        "shortName",
        "trailingPE",
        "recommendationKey",
        "industry",
        "sector",
        "longBusinessSummary",
        "fullTimeEmployees",
        "totalCash",
        "fiftyTwoWeekLow",
        "previousClose",
        "fiftyTwoWeekHigh",
        "dividendYield",
        "marketCap",
    ]

    combined_df: pd.DataFrame = pd.DataFrame()
    desired_columns_combined = [
        "symbol",
        "shortName",
        "trailingPE",
        "priceToSalesTrailing12Months",
        "profitMargins",
        "debtToEquity",
        "totalRevenue",
        "totalCashPerShare",
        "operatingCashflow",
        "totalCash",
        "sharesShort",
        "sharesOutstanding",
    ]

    for comp_symbol in comp_series:
        comp_df: pd.DataFrame = get_company_yahoo(comp_symbol)
        # comp_df = get_company_metrics_fmp(comp_symbol)  # Alternate

        # Fields change according to the data source
        try:
            show_combined_df = pd.concat(
                [
                    show_combined_df,
                    comp_df.loc[
                        :,
                        comp_df.columns.isin(desired_columns_show_combined),
                    ],
                ],
                axis=0,
                ignore_index=True,
            )
        except KeyError as ke:
            logging.warn("Could not find field for %s: %s", comp_symbol, ke)

        # Reorder since `concat` may not have preserved column order.
        show_combined_df = show_combined_df.reindex(
            columns=desired_columns_show_combined
        )

        # Fields change according to the data source
        #
        # NOTE: Yahoo Finance API may use a different symbol such as input
        # 'GOOG' (Class C share with no voting rights) will output 'GOOGL'
        # (Class A share with voting rights).
        try:
            combined_df = pd.concat(
                [
                    combined_df,
                    comp_df.loc[
                        :,
                        comp_df.columns.isin(desired_columns_combined),
                    ],
                ],
                axis=0,
                ignore_index=True,
            )
        except KeyError as ke:
            logging.warn("Could not get metrics for %s: %s: %s", comp_symbol, ke, ke)

    st.write(
        show_combined_df.style.format(
            formatter={
                "trailingPE": "{:,.2f}",
                "totalCash": "${:,.0f}",
                "previousClose": "${:,.2f}",
                "dividendYield": "${:,.2f}",
                "marketCap": "${:,.0f}",
                "sharesOutstanding": "{:,.0f}",
                "fullTimeEmployees": "{:,.0f}",
                "fiftyTwoWeekLow": "${:,.2f}",
                "fiftyTwoWeekHigh": "${:,.2f}",
            }
        )
    )

    # Transform chart
    transformed_combined_df = pd.melt(
        combined_df, id_vars=["symbol", "shortName"], var_name="metric"
    )

    st.write(competitor_ratio_charts(transformed_combined_df, symbol))
