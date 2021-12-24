import os
import random
import string

CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")
SCOPE = "user-library-read playlist-modify-public playlist-modify-private ugc-image-upload"
REDIRECT_URI = "http://127.0.0.1:8080/callback"
AUTH_URL = "https://accounts.spotify.com/api/token"
STATE = "".join(random.choice(string.ascii_lowercase) for _ in range(16))
API_URL = "https://api.spotify.com/v1"
FLASK_PORT = 8080
PLAYLIST_DELETE_LIMIT = 100
DATABASE_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)
DEFAULT_PLAYLIST_NAME = "Recently liked"
