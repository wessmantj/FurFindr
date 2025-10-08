import os
import time
import requests
from datetime import datetime, timedelta

try:
    # Prefer Streamlit secrets when available (deployed environment)
    import streamlit as st
except Exception:
    st = None


def get_api_credentials():
    """Return API credentials, preferring Streamlit secrets then environment variables."""
    api_key = None
    api_secret = None

    if st is not None:
        try:
            api_key = st.secrets['petfinder']['api_key']
            api_secret = st.secrets['petfinder']['api_secret']
        except Exception:
            api_key = None
            api_secret = None

    if not api_key:
        api_key = os.getenv('PETFINDER_API_KEY')
    if not api_secret:
        api_secret = os.getenv('PETFINDER_API_SECRET')

    return api_key, api_secret


class PetfinderClient:
    def __init__(self):
        self.api_key, self.api_secret = get_api_credentials()
        self.base_url = "https://api.petfinder.com/v2"
        self.token = None
        self.token_expires_at = None

    def _request_token(self):
        """Request a new OAuth token from Petfinder."""
        auth_url = f"{self.base_url}/oauth2/token"
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secret
        }
        resp = requests.post(auth_url, data=data)
        resp.raise_for_status()
        body = resp.json()
        self.token = body.get('access_token')
        expires_in = int(body.get('expires_in', 3600))
        self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)

    def _ensure_token(self):
        """Ensure we have a valid token, refreshing if necessary."""
        if self.token and self.token_expires_at:
            # Refresh a few minutes early
            if datetime.now() < (self.token_expires_at - timedelta(minutes=5)):
                return

        self._request_token()

    def _get_headers(self):
        self._ensure_token()
        return {'Authorization': f'Bearer {self.token}'}

    def get_types(self):
        response = requests.get(f"{self.base_url}/types", headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def get_breeds(self, animal_type):
        response = requests.get(f"{self.base_url}/types/{animal_type}/breeds", headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def get_animals(self, location, animal_type=None, limit=20, page=1):
        params = {'location': location, 'limit': limit, 'page': page}
        if animal_type:
            params['type'] = animal_type

        # Small spacing to respect rate limits
        time.sleep(0.02)

        response = requests.get(f"{self.base_url}/animals", headers=self._get_headers(), params=params)
        if response.status_code == 401:
            # Token may have expired - refresh and retry once
            self.token = None
            response = requests.get(f"{self.base_url}/animals", headers=self._get_headers(), params=params)

        response.raise_for_status()
        return response.json()

    def get_organization(self, org_id):
        response = requests.get(f"{self.base_url}/organizations/{org_id}", headers=self._get_headers())
        response.raise_for_status()
        return response.json()
