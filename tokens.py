import os
import requests
import urllib.parse
import webbrowser

from flask import Flask, request, redirect

import constants

app = Flask(__name__)


@app.route("/auth")
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


def shutdown_server():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@app.route("/callback")
def callback():
    if request.args.get("state") != constants.STATE:
        raise RuntimeError("Invalid state from authorization")
    code = request.args.get("code")
    os.environ["AUTH_TOKEN"] = code
    shutdown_server()
    return "Authorization successful"


def get_refresh_token():
    auth_token = get_auth_token()
    refresh_token = exchange_auth_token_for_refresh_token(auth_token)
    print("\nRefresh_token: ", refresh_token)


def get_auth_token():
    webbrowser.open("http://127.0.0.1:8080/auth")
    app.run(port=8080)
    auth_token = os.environ.get("AUTH_TOKEN")
    return auth_token


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


def get_access_token():
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "refresh_token": constants.REFRESH_TOKEN,
            "grant_type": "refresh_token",
            "client_id": constants.CLIENT_ID,
            "client_secret": constants.CLIENT_SECRET,
        },
    )
    if not response.ok:
        raise RuntimeError("Could not obtain token: ", response.content)
    return response.json()["access_token"]