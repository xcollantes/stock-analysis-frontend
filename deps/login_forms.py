"""Login component."""

import streamlit as st

from pyrebase_utils.auth_utils import auth_user, get_auth


def access_account():
    login_form()
    new_user_form()


def login_form() -> None:
    with st.form(key="login_user"):
        email = st.text_input(label="Email")
        password = st.text_input(label="Password", type="password")

        submit = st.form_submit_button("Log in")
        forgot_password = st.form_submit_button("Forgot password")
        if submit:
            if email or password:
                auth_user(email, password)
                st.success("Login success!")

            else:
                st.error("Email and password needed.")


def new_user_form() -> None:
    """Form for creating new account."""
    with st.form(key="new_user"):
        email = st.text_input(label="Email")
        password = st.text_input(label="Password", type="password")
        password_confirm = st.text_input(label="Confirm password", type="password")

        if password != password_confirm:
            st.error("Passwords do not match.")

        submit = st.form_submit_button("Create account")
        if submit:
            get_auth().create_user_with_email_and_password(email, password)
