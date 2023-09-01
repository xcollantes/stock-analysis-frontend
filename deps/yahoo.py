"""Functions for calling Yahoo Finance."""


from datetime import datetime, timedelta
import logging

import streamlit as st
import pandas as pd
import yfinance as yf

from deps.utils import dict_check


@st.cache_data(show_spinner="DEPRECATED ...")
def get_yahoo_metrics(symbol: str) -> tuple[str, str, str, str]:
    """DEPRECATED. Get metrics for a company by calling API.

    These metrics change over time as opposed to the static company data.
    """
    logging.info("API call: Yahoo Finance: select metrics")
    ticker = yf.Ticker(symbol)
    return (
        dict_check(ticker.info, "marketCap"),
        dict_check(ticker.info, "volume"),
        dict_check(ticker.info, "fiftyTwoWeekLow"),
        dict_check(ticker.info, "fiftyTwoWeekHigh"),
    )


@st.cache_data(show_spinner="Querying earnings results ...")
def get_earnings_surprises_yahoo(
    symbol: str, days_ago: int = 365, show_next: bool = True
) -> pd.DataFrame:
    """Return DataFrame with earnings dates and results.

    Also returns next 4 earnings calls. The limit includes the next 4 earnings
    as the latest 4 entries.
    """
    logging.info("API call: Yahoo Finance: Earnings surprises")
    result: pd.DataFrame = pd.DataFrame(
        columns=[
            "EstimatedEarning",
            "ActualEarning",
            "SurprisePercent",
        ]
    )

    ticker = yf.Ticker(symbol)

    if ticker:
        earnings_dates = ticker.get_earnings_dates(
            limit=20
        )  # Include future earnings dates always
        if earnings_dates is not None:
            earning_df = earnings_dates.rename(
                columns={
                    "EPS Estimate": "EstimatedEarning",
                    "Reported EPS": "ActualEarning",
                    "Surprise(%)": "SurprisePercent",
                }
            )
            earning_df["Date"] = earning_df.index
            if show_next:
                # Drop if no result and no expected for future earnings dates
                result = earning_df.dropna(subset=["EstimatedEarning"]).reset_index(
                    drop=True
                )
            else:
                # Drop if no future earnings dates
                result = earning_df.dropna(subset=["ActualEarning"]).reset_index(
                    drop=True
                )

            # Result from Yahoo Finance is unpredictable: 4 max future earnings
            # or fewer so take the 20 last periods and cut earliest dates to fit
            # graph
            result = result[
                result["Date"]
                >= (datetime.now() - timedelta(days_ago)).strftime("%Y-%m-%d")
            ]

    else:
        logging.error("Could not get earnings from Yahoo.")

    return result


@st.cache_data(show_spinner="Querying historical prices ...")
def get_historic_prices(ticker_symbol: str, days_ago: int) -> pd.DataFrame:
    """Given a date range, returns historical price range.

    Yahoo Finance API does not have weekends since markets are closed but the
    `days_ago` parameter will count only market open days.

    Args:
      ticker_symbol: String of ticker.
      days_ago: Range of stock history prior to today.

    Returns:
      Historical data.
    """
    days_ago -= (days_ago // 7) * 2  # Subtract weekends

    logging.info("API call: Yahoo API: historic prices")
    df: pd.DataFrame = yf.Ticker(ticker_symbol.upper())
    history = df.history(period=f"{days_ago}d")
    history["DateCloseET"] = history.index  # Add non-index field

    history["PercentChange"] = history["Close"].pct_change()

    return history


@st.cache_data(show_spinner="Converting metrics data frame ...")
def handle_filter_metrics(ratio_df: pd.DataFrame) -> pd.DataFrame:
    """Get only specific column metrics."""
    result_df: pd.DataFrame = pd.DataFrame()
    try:
        result_df = ratio_df[
            [
                "symbol",
                "grossProfits",
                "revenueGrowth",
                "freeCashflow",
                "grossMargins",
                "operatingMargins",
                "trailingPegRatio",
            ]
        ]
    except KeyError:
        # If company has no columns for these metrics
        pass

    return result_df


@st.cache_data(show_spinner="Querying company data ...")
def get_company_yahoo(symbol: str) -> pd.DataFrame:
    """Get all financial metrics, company details, and filing info for a company."""
    result_df: pd.DataFrame = pd.DataFrame()

    try:
        logging.info("API call: Yahoo Finance: Company ratios")
        ticker = yf.Ticker(symbol)
        result_df = pd.json_normalize(ticker.info)
        # result_df.rename(columns={"underlyingSymbol": "symbol"}, inplace=True)
    except Exception as he:
        logging.error(he)

    return result_df
