"""Pyrebase/Firebase Auth utils."""

import streamlit as st
from streamlit.components.v1 import html
import pyrebase


config = {
    "apiKey": st.secrets.pyrebase_firebase.apiKey,
    "authDomain": st.secrets.pyrebase_firebase.authDomain,
    "databaseURL": st.secrets.pyrebase_firebase.databaseURL,
    "storageBucket": st.secrets.pyrebase_firebase.storageBucket,
}


firebase_app = pyrebase.initialize_app(config)


def get_auth():
    """Return Pyrebase auth."""
    return firebase_app.auth()


def reset_password(email: str):
    """Forgot password."""
    with st.spinner("Sending password reset email ..."):
        get_auth().send_password_reset_email(email)


def auth_user(email: str, password: str) -> any:
    """Determine authentication for a user."""
    with st.spinner("Logging in ..."):
        user = get_auth().sign_in_with_email_and_password(email, password)
        return user


def redirect(page_name, timeout_secs=3):
    """Workaround for redirecting within app.

    Args:
        page_name: Must be the encoded page URL as found in the browser bar.
            Example: /Top%20drops
        timeout_secs: Timeout for redirect in seconds.
    """
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (
        page_name,
        timeout_secs,
    )
    html(nav_script)
