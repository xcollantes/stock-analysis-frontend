"""Chart visualizations."""


import altair as alt
import pandas as pd

import streamlit as st

WIDTH = 2100


def stock_chart_trad_mult(symbol_data: pd.DataFrame, title: str = "") -> alt.Chart:
    """Show multi-line graph for a many stock symbols.

    Column names must match the source data from Yahoo Finance historical prices.

    Required columns:
        Name - Company name
        PercentChange - Previous delta from day before
        Close - Closing price for stock
        DateCloseET - Day for closing price in Eastern Time

    Args:
      symbol_data: DataFrame with Close, DateCloseET, Symbol, Name,
      Percent Change.
      title: Optional chart title header.

    Returns:
      Altair graph.
    """
    x_axis = alt.X("DateCloseET:T", axis=alt.Axis(labelAngle=-50))
    y_axis = alt.Y(
        "Close",
        scale=alt.Scale(
            domain=[symbol_data["Close"].min(), symbol_data["Close"].max()]
        ),
        title="Close price",
    )

    color = alt.Color("Name:N", legend=None)
    selection = alt.selection_multi(
        fields=["DateCloseET"],
        nearest=True,
        on="mouseover",
        empty="none",
        clear="mouseout",
    )
    selection_opacity = alt.condition(selection, alt.value(1), alt.value(0))

    tooltip = [
        alt.Tooltip("Name:N"),
        #  alt.Tooltip("Symbol:N"),
        #  alt.Tooltip("Sector:N"),
        #  alt.Tooltip("Industry:N"),
        alt.Tooltip("PercentChange:Q", format=".2%"),
        alt.Tooltip("DateCloseET:T"),
        alt.Tooltip("Close", format="$.2f"),
    ]

    change_chart = (
        alt.Chart(symbol_data)
        .mark_line()
        .encode(
            x=x_axis,
            y=y_axis,
            color=color,
            tooltip=tooltip,
        )
        .properties(
            title={"text": title, "subtitle": f"{title}"},
        )
    )

    horizontal_marker = (
        alt.Chart(symbol_data)
        .mark_rule(strokeWidth=2, color="red")
        .encode(
            x=x_axis,
            opacity=selection_opacity,
            tooltip=tooltip,
        )
        .add_selection(selection)
    )

    return alt.layer(change_chart, horizontal_marker)


def competitor_ratio_charts(ratio_df: pd.DataFrame, base_symbol: str) -> alt.Chart:
    """Return Altair chart comparing financial ratios.

    Args:
        ratio_df: DataFrame with symbols of competitors including the original
            stock symbol to compare against.
            Required columns:
                symbol - Company symbol
                value - Metric value
                metric - Accounting measurement name (FreeFlowCash, P/E,
                GrossProfits, etc.)
        base_symbol: Baseline stock symbol to compare against.

    Returns:
        Altair graph layered on mark charts for each competitor including the
        base symbol.
    """
    if ratio_df.shape[0] < 1:
        return alt.Chart()

    base_symbol = base_symbol.upper()
    marker_shape: list[str] = []
    for distinct_symbol in ratio_df["symbol"].drop_duplicates().sort_values():
        if distinct_symbol == base_symbol:
            marker_shape.append(
                "M0,.5L.6,.8L.5,.1L1,-.3L.3,-.4L0,-1L-.3,-.4L-1,-.3L-.5,.1L-.6,.8L0,.5Z"
            )  # Star SVG path
        else:
            marker_shape.append("circle")

    chart = (
        alt.Chart(ratio_df)
        .mark_point(
            size=50,
            strokeWidth=6,
        )
        .encode(
            row=alt.Row("metric:N", header=alt.Header(labelAngle=0, labelFontSize=12)),
            x=alt.X("value:Q"),
            y=alt.Y("symbol:N"),
            tooltip=alt.Tooltip(["shortName:N", "metric:N", "value:Q"]),
            shape=alt.Shape(
                "symbol:N", scale=alt.Scale(range=marker_shape), legend=None
            ),
            color=alt.Color(
                "shortName:N",
                legend=alt.Legend(orient="top"),
            ),
        )
    ).resolve_scale(x="independent")

    return chart


def earnings_beat_chart(earnings_df: pd.DataFrame, symbol_name: str = ""):
    """Altair chart with circles for expected and actual earnings.

    Required columns:
        Date
        EstimatedEarning
        ActualEarning
    """
    point_size: int = 200
    stroke_size: int = 4
    date_filter: str = "year(datum.Date) > year(now()) - 5"

    if symbol_name != "":
        symbol_name = f"({symbol_name})"

    x_axis = alt.X("Date:T")
    tooltip = alt.Tooltip(["Date:T", "EstimatedEarning:Q", "ActualEarning:Q"])

    expected_chart = (
        alt.Chart(earnings_df)
        .mark_point(size=point_size, strokeWidth=stroke_size, color="gray")
        .encode(
            x=x_axis,
            y=alt.Y(
                "EstimatedEarning:Q",
                axis=alt.Axis(labels=True),
            ),
            tooltip=tooltip,
        )
        .transform_filter(date_filter)
    )

    actual_chart = (
        alt.Chart(earnings_df)
        .mark_point(size=point_size, strokeWidth=stroke_size, color="green")
        .encode(
            x=x_axis,
            y=alt.Y("ActualEarning:Q", axis=alt.Axis(labels=False)),
            tooltip=tooltip,
        )
        .transform_filter(date_filter)
    )

    return expected_chart + actual_chart


def _DEPRECATED_format_company_description(
    company_info_df: pd.DataFrame,
) -> dict[str, str]:
    """Handle errors if field does not exist for company info.

    DEPRECATED: Remove if after 01 Oct 2023.
    """
    return {
        "longName": company_info_df["longName"].values[0],
        "longBusinessSummary": company_info_df["longBusinessSummary"].values[0],
        "industry": company_info_df["industry"].values[0],
        "sector": company_info_df["sector"].values[0],
        "address1": company_info_df["address1"].values[0],
        "city": company_info_df["city"].values[0],
        "state": company_info_df["state"].values[0],
        "country": company_info_df["country"].values[0],
        "fullTimeEmployees": company_info_df["fullTimeEmployees"].values[0],
        "website": company_info_df["website"].values[0],
    }
