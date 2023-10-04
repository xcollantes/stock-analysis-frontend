"""Utils for checking passphrase."""

import streamlit as st


def is_auth(main, url_args) -> None:
    """Checks for URL args to match passphrase.

    Args:
        main: Function to run once authenticated.

    Returns:
        Renders either the given next authenticated function or an access denied
       visual.
    """
    try:
        if url_args["p"][0] in st.secrets.passphrases.p:
            return main()
        return show_login()
    except KeyError:
        return show_login()


def show_login() -> None:
    """Render password box."""
    st.header("Enter passphrase")
    with st.form(key="passphrase_form"):
        phrase_attempt: str = st.text_input(label="").strip()
        submit = st.form_submit_button(label="Enter")

    if submit:
        if phrase_attempt in st.secrets.passphrases.p:
            st.success("Login success. Please refresh page.")
            st.experimental_set_query_params(p=phrase_attempt)
        else:
            st.error("Wrong passphrase")
