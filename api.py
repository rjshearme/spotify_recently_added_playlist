import json
import requests

import constants
import tokens


def make_api_call(access_token, url, method, **kwargs):
    response = method(
        url=url,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
        **kwargs,
    )
    if not response.ok:
        raise RuntimeError(f"Error making request to {url}: ", response.content)
    return response


def get_user_id_and_name_from_refresh_token(refresh_token):
    access_token = tokens.get_access_token(refresh_token)
    user_response = make_api_call(access_token, constants.API_URL + "/me", requests.get)
    return user_response.json()["id"], user_response.json()["display_name"]


def make_new_playlist(user):
    response = make_api_call(
        user.access_token,
        url=f"{constants.API_URL}/users/{user.user_id}/playlists",
        method=requests.post,
        data=json.dumps({"name": constants.DEFAULT_PLAYLIST_NAME, "description": f"Here are your most recently added songs from the last {user.recently_added_delta_days} days"})
    )
    return response.json()["id"]
