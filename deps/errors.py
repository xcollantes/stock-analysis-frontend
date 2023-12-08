"""Form errors."""


import re


def symbol_has_error(symbol_query: str) -> str:
    """Check stock query is valid, if not returns error message."""
    if symbol_query == "":
        return "Enter stock symbol"
    if not bool(re.match("^[a-zA-Z]+$", symbol_query)):
        return "Letters only"
    if not len(symbol_query) <= 5:
        return "More than 4 characters"

    return ""
