"""Bard API calls."""


from bardapi import Bard
import streamlit as st

BARD_TOKEN: str = st.secrets.bard.token


def get_drop_reason(company: str) -> str:
    """Ask Google Bard why a certain company has dropped in price.

    Args:
        company: Symbol or name of company to find reason for shock.

    Return:
        Bard response.
    """
    bard = Bard(token=BARD_TOKEN)
    return bard.get_answer(
        f"What is the main driving cause for the stock {company} to decrease in price today?"
    )["content"]
