import requests
import urllib.parse

from flask import Flask, request, redirect, url_for, render_template

import constants
import models
import playlists

app = Flask(__name__)


@app.route("/")
def auth():
    vars_ = {
        "response_type": "code",
        "client_id": constants.CLIENT_ID,
        "scope": constants.SCOPE,
        "redirect_uri": constants.REDIRECT_URI,
        "state": constants.STATE,
    }
    redirect_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(vars_)
    return redirect(redirect_url, 302)


@app.route("/callback")
def callback():
    if request.args.get("state") != constants.STATE:
        raise RuntimeError("Invalid state from authorization")
    auth_token = request.args.get("code")
    refresh_token = exchange_auth_token_for_refresh_token(auth_token)
    user_id = models.create_user(refresh_token)
    return redirect(url_for("settings", user_id=user_id))


@app.route("/settings/<user_id>", methods=["GET", "POST"])
def settings(user_id):
    if request.method == "GET":
        return render_template("settings.html", user_id=user_id)
    elif request.method == "POST":
        recently_added_delta_days = request.form.get("recently_added_delta_days")
        user = models.update_user(user_id, recently_added_delta_days=recently_added_delta_days)
        playlists.generate_playlist(user)
        return render_template("settings_updated.html", user=user)


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


def get_access_token(user):
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "refresh_token": user.refresh_token,
            "grant_type": "refresh_token",
            "client_id": constants.CLIENT_ID,
            "client_secret": constants.CLIENT_SECRET,
        },
    )
    if not response.ok:
        raise RuntimeError("Could not obtain token: ", response.content)
    return response.json()["access_token"]


if __name__ == "__main__":
    app.run(debug=True, port=8080)