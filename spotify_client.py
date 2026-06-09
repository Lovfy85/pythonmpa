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


def extract_genres(sp, limit=50):
    """
    Get that of the genres that the user listens to based on the user's top artists.
    """

    #This is to get that of the user's top artists.
    results = sp.current_user_top_artists(
        limit = limit,
        time_range = "long_term"
    )

    #Stores the user's top artists.
    items = results.get("items", [])
    
    #Gets that of the genre's counted based on the artist's connection to their genre.
    genre_counts = {}

    #Go through each artist to which then, get that of their respective genres.
    for artist in items:
        artist_genres = artist.get("genres", [])

        #Go through each genre where if it has not been counted yet, initialized it
        # to be counted. If it has been counted before, increase it by one based on how
        # much it was counted before. 
        for genre in artist_genres:

            if genre in genre_counts:
                genre_counts[genre] += 1

            else:
                genre_counts[genre] = 1

    #This is to then get that of the genres counted overall. 
    return genre_counts


def build_music_profile(top_artists, top_tracks, genres):
    """
    This makes the music profile based on the user's top artists, tracks and genres.
    """

    profile = {
        "top_artists": top_artists,
        "top_tracks": top_tracks, 
        "genres": genres
    }

    return profile