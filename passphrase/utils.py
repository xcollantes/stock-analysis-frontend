"""Utils for checking passphrase."""

import streamlit as st
from google.cloud import secretmanager


def is_auth(main, url_args):
    """Checks for URL args to match passphrase.

    Args:
        main: Function to run once authenticated.

    Returns:
        Renders either the given next authenticated function or an access denied
       visual.
    """
    try:
        if matches_passphrase(url_args["p"][0]):
            return main()
        return access_denied()
    except KeyError:
        return access_denied()


@st.cache_data(show_spinner=False)
def matches_passphrase(candidate: str) -> bool:
    """Check if passphrase is correct."""
    with st.spinner("Verifying authentication ..."):
        return get_passphrase() == candidate


def access_denied():
    """Visual for access denied."""
    st.header("Access is denied")


def get_passphrase() -> str:
    """Get secret passphrase."""
    secret_id = st.secrets.gcp_secrets.endpoint
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(request={"name": secret_id})
    return response.payload.data.decode("UTF-8")
