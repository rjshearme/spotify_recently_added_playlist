import datetime
import json
import requests

import api
import constants
from tracks import Track
import models


def list_users():
    users = models.get_all_entries()
    for user in users:
        print(user)


def generate_playlists():
    users = models.get_all_entries()
    for user in users:
        generate_playlist(user)
    

def generate_playlist(user):
    user = make_playlist(user)
    existing_playlist_tracks = get_playlist_tracks(user)
    delete_playlist_tracks(user, existing_playlist_tracks)
    new_playlist_tracks = get_liked_tracks(user)
    post_new_playlist(user, new_playlist_tracks)
    update_playlist_description(user)


def update_playlist_description(user):
    api.make_api_call(
        user.access_token,
        url=f"{constants.API_URL}/playlists/{user.playlist_id}",
        method=requests.put,
        data=json.dumps({"description": f"Here are your most recently added songs from the last {user.recently_added_delta_days} days"})
    )


def make_playlist(user):
    user = models.get_playlist_id(user)
    set_playlist_image(user)
    return user


def set_playlist_image(user):
    with open("static/images/playlist_cover_image.b64", "rb") as fh:
        image_data = fh.read()
    api.make_api_call(user.access_token, url=f"{constants.API_URL}/playlists/{user.playlist_id}/images", method=requests.put, data=image_data)


def get_liked_tracks(user):
    cutoff_date = datetime.date.today() - datetime.timedelta(days=user.recently_added_delta_days)
    new_playlist_tracks = []
    page_index = 0
    cut_off_date_reached = False
    while not cut_off_date_reached:
        next_tracks = get_tracks_by_page(user, page=page_index)
        for track in next_tracks:
            if track.day_added < cutoff_date:
                cut_off_date_reached = True
                break
            new_playlist_tracks.append(track)
        page_index += 1
    return new_playlist_tracks


def get_tracks_by_page(user, page):
    params = {
        "limit": 50,
        "offset": page*50,
    }
    url = constants.API_URL + "/me/tracks?"
    response = api.make_api_call(user.access_token, url, requests.get, params=params)
    return [Track(item) for item in response.json()["items"]]


def post_new_playlist(user, tracks):
    request_bodies = [tracks[n:n + constants.PLAYLIST_DELETE_LIMIT] for n in range(0, len(tracks), constants.PLAYLIST_DELETE_LIMIT)]
    for request_body in request_bodies:
        params = "uris=" + ",".join([f"spotify:track:{track.track_id}" for track in request_body])
        url = constants.API_URL + f"/playlists/{user.playlist_id}/tracks?" + params
        api.make_api_call(user.access_token, url, requests.post)


def delete_playlist_tracks(user, tracks):
    request_bodies = [tracks[n:n+constants.PLAYLIST_DELETE_LIMIT] for n in range(0, len(tracks), constants.PLAYLIST_DELETE_LIMIT)]
    for request_body in request_bodies:
        url = constants.API_URL + f"/playlists/{user.playlist_id}/tracks"
        data = json.dumps({"tracks": [{"uri": f"spotify:track:{track.track_id}"} for track in request_body]})
        api.make_api_call(user.access_token, url, requests.delete, data=data)


def get_playlist_tracks(user):
    playlist_tracks = []
    page_index = 0
    url = constants.API_URL + f"/playlists/{user.playlist_id}/tracks"

    while True:
        params = {
            "limit": 50,
            "offset": page_index * 50,
            "fields": "items(added_at, track(name, id))"
        }
        response = api.make_api_call(user.access_token, url, requests.get, params=params)
        if not response.json()["items"]:
            break

        playlist_tracks += [Track(item) for item in response.json()["items"]]
        page_index += 1
    return playlist_tracks
