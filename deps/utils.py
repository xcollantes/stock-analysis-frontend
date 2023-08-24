"""Util data processing functions."""


import pandas as pd


def filter_by_symbol(agg_stock_df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    return agg_stock_df[agg_stock_df["Symbol"] == symbol]


def dict_check(check, key) -> any:
    """Convert invalid JSON `undefined` into null to avoid error."""
    try:
        return check[key]
    except KeyError:
        return None
