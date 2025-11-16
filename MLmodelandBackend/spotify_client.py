# spotify_client.py
# minimal spotify helper using Client Credentials flow

import os
import time
import requests
from typing import Dict

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

class SpotifyClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self._token = None
        self._token_expiry = 0

    def _fetch_token(self):
        resp = requests.post(
            SPOTIFY_TOKEN_URL,
            data={"grant_type": "client_credentials"},
            auth=(self.client_id, self.client_secret),
        )
        resp.raise_for_status()
        data = resp.json()
        self._token = data["access_token"]
        self._token_expiry = time.time() + data.get("expires_in", 3600) - 60

    def get_token(self):
        if not self._token or time.time() >= self._token_expiry:
            self._fetch_token()
        return self._token

    def get(self, path: str, params: Dict = None):
        token = self.get_token()
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(f"https://api.spotify.com/v1{path}", headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()
