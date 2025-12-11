import streamlit as st
import requests
import urllib.parse

DRIBBBLE_AUTH_URL = "https://dribbble.com/oauth/authorize"
DRIBBBLE_TOKEN_URL = "https://dribbble.com/oauth/token"
DRIBBBLE_USER_URL = "https://api.dribbble.com/v2/user"


def get_auth_url():
    client_id = st.secrets["dribbble_client_id"]

    redirect_uri = (
        "https://covid-vaccine-tracker-2025.streamlit.app/dribbble/callback"
    )

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "public upload",
    }

    return f"{DRIBBBLE_AUTH_URL}?{urllib.parse.urlencode(params)}"


def exchange_code_for_token(code: str):
    payload = {
        "client_id": st.secrets["dribbble_client_id"],
        "client_secret": st.secrets["dribbble_client_secret"],
        "code": code,
    }

    response = requests.post(DRIBBBLE_TOKEN_URL, data=payload)

    if response.status_code == 200:
        return response.json().get("access_token")

    return None


def fetch_dribbble_profile(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(DRIBBBLE_USER_URL, headers=headers)

    if response.status_code == 200:
        return response.json()

    return None


def logout():
    if "dribbble_token" in st.session_state:
        del st.session_state["dribbble_token"]

    if "dribbble_user" in st.session_state:
        del st.session_state["dribbble_user"]
