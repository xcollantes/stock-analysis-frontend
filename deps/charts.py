"""Charts."""


import altair as alt
import pandas as pd
import streamlit as st

from deps.chart_components import earnings_beat_chart, stock_chart_trad_mult
from deps.yahoo import (
    get_company_yahoo,
    get_earnings_surprises_yahoo,
    get_historic_prices,
)


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

    # competitor_list: pd.Series = get_competitors(symbol)

    # competitors_ratio_df: pd.DataFrame = handle_filter_metrics(info_df)
    # for competitor_symbol in competitor_list:
    #     ratio_df: pd.DataFrame = get_company_yahoo(competitor_symbol)
    #     ratio_df = handle_filter_metrics(ratio_df)

    #     competitors_ratio_df = pd.concat(
    #         [competitors_ratio_df, ratio_df],
    #         axis=0,
    #         ignore_index=True,
    #     )

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
