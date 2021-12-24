import requests

import constants


def exchange_auth_token_for_refresh_token(auth_token):
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "code": auth_token,
            "redirect_uri": constants.REDIRECT_URI,
            "grant_type": "authorization_code",
            "client_id": constants.CLIENT_ID,
            "client_secret": constants.CLIENT_SECRET,
        },
    )
    return response.json()["refresh_token"]


def get_access_token(refresh_token):
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "client_id": constants.CLIENT_ID,
            "client_secret": constants.CLIENT_SECRET,
        },
    )
    if not response.ok:
        raise RuntimeError("Could not obtain token: ", response.content)
    return response.json()["access_token"]