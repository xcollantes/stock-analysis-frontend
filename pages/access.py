# -*- coding: utf-8 -*-

import os

# import flask
import requests

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery


def main():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "./oauth.json",
        scopes=["https://www.googleapis.com/auth/secretmanager.secretAccessor"],
    )
    flow.redirect_uri = "https://www.example.com/oauth2callback"

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type="offline",
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes="true",
    )
    print("AUTH URL: ", authorization_url)


if __name__ == "__main__":
    main()
