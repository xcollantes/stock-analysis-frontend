"""Pyrebase/Firebase Auth utils."""

import streamlit as st
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
    get_auth().send_password_reset_email(email)


def auth_user(email: str, password: str) -> any:
    """Determine authentication for a user."""

    user = get_auth().sign_in_with_email_and_password(email, password)
    print(user)
    return user
