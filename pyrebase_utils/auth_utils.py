"""Pyrebase/Firebase Auth utils."""

import streamlit as st
import pyrebase


config = {
    "apiKey": st.secrets.pyrebase_firebase.apikey,
    "authDomain": st.secrets.pyrebase_firebase.authDomain,
    "databaseURL": st.secrets.pyrebase_firebase.databaseURL,
    "storageBucket": st.secrets.pyrebase_firebase.storageBucket,
}


firebase_app = pyrebase.initialize_app(config)


def get_auth():
    """Return Pyrebase auth."""
    return firebase_app.auth()


def auth_user(email: str, password: str) -> any:
    """Determine authentication for a user."""

    user = auth.sign_in_with_email_and_password(email, password)
    print(user)
    return user
