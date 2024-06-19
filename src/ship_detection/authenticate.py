import json
from google.oauth2 import credentials as credentials_lib
from google.auth.transport.requests import Request
import streamlit

def authorize():
    creds = credentials_lib.Credentials(
        token = streamlit.secrets["token"],
        refresh_token = streamlit.secrets["refresh_token"],
        token_uri = streamlit.secrets["token_uri"],
        client_id = streamlit.secrets["client_id"],
        client_secret = streamlit.secrets["client_secret"],
        scopes = streamlit.secrets["scopes"]
    )

    return creds
