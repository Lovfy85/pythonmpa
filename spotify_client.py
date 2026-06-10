import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE

def authenticate_user():
    """
    This is to make the user to be logged in from Spotify to sync up their
    information to be gotten overall.
    """

    #This whole block is to get the information needed from what was established in 
    # config.py.
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id = CLIENT_ID, 
            client_secret = CLIENT_SECRET,
            redirect_uri = REDIRECT_URI,
            scope = SCOPE, 
            show_dialog = True,
            cache_path = ".cache"
        )
    )

    #This is to get that of the user to be gotten based on the authentication. 
    user = sp.current_user()

    #This goes over a simple check where if the user can log in or not to get their 
    # information of the songs they listen to. 
    if not user:
        raise Exception("Failure in authorizing the supposed user overall.");
    print(f"The user is now logged in as: {user['display_name']}")
    return sp


def get_top_artists(sp, limit=5):
    """
    This is to get that of the top 5 artists from the Spotify user.
    """
    

    #This is to get that of the Spotify user's top 5 artists of all time. 
    results = sp.current_user_top_artists(
        limit = limit,
        time_range = "long_term"
    )

    #Stores the user's top 5 artists. 
    items = results.get("items", [])

    #This is to store that of the artists to be displayed.
    top_artists = []
    
    #For that of the artists to get in the items, get them and have them to 
    # added inside of the 'top_artists' list. Return after. 
    for artist in items:
        artist_name = artist.get("name")

        if artist_name is not None: 
            top_artists.append(artist_name)

    return top_artists


def get_top_tracks(sp, limit=5):
    """
    This is to get that of the top 5 tracks from the Spotify user.
    """

    #This is to get that of the Spotify user's top 5 tracks of all time. 
    results = sp.current_user_top_tracks(
        limit = limit,
        time_range = "long_term"
    )

    #Stores the user's top 5 tracks.
    items = results.get("items", [])

    #This is to store that of the artists to be displayed. 
    top_tracks = []

    #For that of the tracks to get in the items, get them and have them to 
    # added inside of the 'top_tracks' list. Return after. 
    for track in items: 
        track_name = track.get("name")

        if track_name is not None:
            top_tracks.append(track_name)

    return top_tracks


def build_music_profile(top_artists, top_tracks):
    """
    This makes the music profile based on the user's top artists and tracks. 
    """

    profile = {
        "top_artists": top_artists,
        "top_tracks": top_tracks, 
    }

    return profile