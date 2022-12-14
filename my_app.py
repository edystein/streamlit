import streamlit as st

from google.oauth2 import service_account
from google.cloud import storage

from common.authentication import authenticate


# Create API client.
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
client = storage.Client(credentials=credentials)

# authentication
name, authentication_status, user_name, authenticator, b_authentication_ok = authenticate()

st.title('Welcome to the Stein app 🎈')
