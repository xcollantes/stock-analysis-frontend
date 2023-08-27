"""Login page."""


import streamlit as st

from deps.page_config import PageConfig
from pyrebase_utils.auth_utils import auth_user, get_auth, reset_password

PageConfig(initial_sidebar_state="collapsed", layout="centered").get_config()


def main():
    # show_create_account: bool = st.button("Create account", use_container_width=True)

    with st.form(key="login_user"):
        email = st.text_input(label="Email")
        password = st.text_input(label="Password", type="password")

        submit = st.form_submit_button("Log in")
        forgot_password = st.form_submit_button("Forgot password")

        if submit:
            if email and password:
                auth_user(email, password)
                st.success("Login success!")

            else:
                st.error("Email and password needed.")
        if forgot_password:
            if email:
                reset_password(email)
                st.success("Check your email for password reset.")
            else:
                st.warning("Enter email")

    # Could not put each form in a function and reference form parts.  Form
    # submit did not recognize as form.
    # if show_create_account:
    #     with st.form(key="new_user_and_login"):
    #         new_email = st.text_input(label="Email")
    #         new_password = st.text_input(label="Password", type="password")
    #         new_password_confirm = st.text_input(
    #             label="Confirm password", type="password"
    #         )

    #         new_submit = st.form_submit_button(label="Create account")
    #         if new_submit:
    #             print(new_email)
    #             if new_password != new_password_confirm:
    #                 st.error("Passwords do not match.")
    #             else:
    #                 x = get_auth().create_user_with_email_and_password(
    #                     new_email, new_password
    #                 )
    #                 print("ACCOUNT CREATED: ", x)

    # else:
    #     with st.form(key="login_user"):
    #         email = st.text_input(label="Email")
    #         password = st.text_input(label="Password", type="password")

    #         submit = st.form_submit_button("Log in")

    #         # if not show_create_account:
    #         #     forgot_password = st.form_submit_button("Forgot password")

    #         if submit:
    #             if email and password:
    #                 print(submit)
    #                 auth_user(email, password)
    #                 st.success("Login success!")

    #             else:
    #                 st.error("Email and password needed.")


if __name__ == "__main__":
    main()
