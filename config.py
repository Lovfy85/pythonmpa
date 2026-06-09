import os

#This is to get that of the Spotify API credentials. This is done in order 
# to get the information needed for the app. 
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "dbd0937a5b4c4cf3b563f62802ff751f");
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "14a3cb01b91d416a95f6957a9aabb5d2")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8501/callback")

#This is to establish that of the requests needed from the API. 
SCOPE = "user-top-read user-read-recently-played"

#The name that was established in that of the developer dashboard in Spotify website
# for this app in use overall. 
APP_NAME = "pythonmpa"