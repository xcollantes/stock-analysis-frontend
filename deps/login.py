"""Login component."""

from firebase.auth_utils import auth_user
import streamlit as st


with st.form(key="login"):
    email = st.text_input(label="Email")
    password = st.text_input(label="Password")

    submit = st.form_submit_button("Log in")
    forgot_password = st.form_submit_button("Log in")
    if submit:
        if email or password:
            auth_user()
        else:
            st.error("Email and password needed.")
