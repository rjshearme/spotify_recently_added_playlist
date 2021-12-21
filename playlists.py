import datetime
import json
import requests

import constants
import tokens
from tracks import Track


def generate_playlist(days_limit):
    existing_playlist_tracks = get_playlist_tracks()
    delete_playlist_tracks(existing_playlist_tracks)
    new_playlist_tracks = get_liked_tracks(days_limit=days_limit)
    post_new_playlist(new_playlist_tracks)


def get_liked_tracks(days_limit):
    cutoff_date = datetime.date.today() - datetime.timedelta(days=days_limit)
    new_playlist_tracks = []
    page_index = 0
    cut_off_date_reached = False
    while not cut_off_date_reached:
        next_tracks = get_tracks_by_page(page=page_index)
        for track in next_tracks:
            if track.day_added < cutoff_date:
                cut_off_date_reached = True
                break
            new_playlist_tracks.append(track)
        page_index += 1
    return new_playlist_tracks


def get_tracks_by_page(page):
    access_token = tokens.get_access_token()
    request_params = {
        "limit": 50,
        "offset": page*50,
    }
    response = requests.get(
        url=constants.API_URL + "me/tracks?",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
        params=request_params
    )
    return [Track(item) for item in response.json()["items"]]


def post_new_playlist(tracks):
    access_token = tokens.get_access_token()
    request_bodies = [tracks[n:n + constants.PLAYLIST_DELETE_LIMIT] for n in range(0, len(tracks), constants.PLAYLIST_DELETE_LIMIT)]
    for request_body in request_bodies:
        params = "uris=" + ",".join([f"spotify:track:{track.track_id}" for track in request_body])
        requests.post(
            url=constants.API_URL + f"playlists/{constants.PLAYLIST_ID}/tracks?" + params,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )


def delete_playlist_tracks(tracks):
    access_token = tokens.get_access_token()
    request_bodies = [tracks[n:n+constants.PLAYLIST_DELETE_LIMIT] for n in range(0, len(tracks), constants.PLAYLIST_DELETE_LIMIT)]
    for request_body in request_bodies:
        requests.delete(
            url=constants.API_URL + f"playlists/{constants.PLAYLIST_ID}/tracks",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
            data=json.dumps({
                "tracks": [{"uri": f"spotify:track:{track.track_id}"} for track in request_body]
            })
        )


def get_playlist_tracks():
    playlist_tracks = []
    page_index = 0

    access_token = tokens.get_access_token()
    while True:
        request_params = {
            "limit": 50,
            "offset": page_index * 50,
            "fields": "items(added_at, track(name, id))"
        }

        response = requests.get(
            url=constants.API_URL + f"playlists/{constants.PLAYLIST_ID}/tracks",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
            params=request_params,
        )
        if not response.json()["items"]:
            break

        playlist_tracks += [Track(item) for item in response.json()["items"]]
        page_index += 1
    return playlist_tracks
