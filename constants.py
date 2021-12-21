import os
import random
import string

REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")
SCOPE = "user-library-read playlist-modify-public playlist-modify-private"
REDIRECT_URI = "http://127.0.0.1:8080/callback"
AUTH_URL = "https://accounts.spotify.com/api/token"
STATE = "".join(random.choice(string.ascii_lowercase) for _ in range(16))
API_URL = "https://api.spotify.com/v1/"
FLASK_PORT = 8080
USER_ID = os.getenv("USER_ID")
PLAYLIST_ID = os.getenv("PLAYLIST_ID")
PLAYLIST_DELETE_LIMIT = 100