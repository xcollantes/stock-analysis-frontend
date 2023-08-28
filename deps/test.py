import streamlit as st
from google.cloud import secretmanager
from google.oauth2 import service_account


secret_id = st.secrets.gcp_secrets.endpoint
client = secretmanager.SecretManagerServiceClient()
response = client.access_secret_version(request={"name": secret_id})
print(response.payload.data.decode("UTF-8"))
