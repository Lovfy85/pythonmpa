import spotipy
from spotipy.oauth2 import SpotifyOAuth

from lastfm_client import get_artist_tags
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE

import os
import time

#This is to store that of cache gotten from Spotify and Last.fm.
# This is used for that of getting genres from both APIs.
_artist_genre_cache = {}
_lastfm_cache = {}


def authenticate_user():

    """
    Logs the user into Spotify and returns an authenticated client.
    """

    #This is the formatted structure to get auhenticated for the app
    # through a Spotify account.
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        show_dialog=True,

        #Stores Spotify login token properly so user is NOT re-prompted every rerun
        cache_path=".spotify_cache"
    )

    #Manages how long to authroize a user for. 
    sp = spotipy.Spotify(
        auth_manager=auth_manager,
        requests_timeout=60
    )

    #This is to check if a user to be logged in is valid or not.
    user = sp.current_user()
    if not user:
        raise Exception("Authentication failed.")

    print(f"Logged in as: {user['display_name']}")

    return sp


def get_top_artists(sp, limit=20):

    """
    Fetch the user's top artists from Spotify.
    """

    #This is to get that of the top 20 artists and to be stored as items in
    # an array list.
    results = sp.current_user_top_artists(
        limit=limit,
        time_range="long_term"
    ).get("items", [])

    #This is where to store that of the artists overall.
    top_artists = []

    #For each artist that was gotten in results list...
    for artist in results:

        #Get that of the artist's id and name.
        artist_id = artist.get("id")
        artist_name = artist.get("name")

        #If cannot get an artist's id or name, move unto the next.
        if not artist_id or not artist_name:
            continue

        #To add that artist into the top artists list.
        top_artists.append({
            "id": artist_id,
            "name": artist_name,

            #Genres already come from this response sometimes
            "genres": artist.get("genres", [])
        })

    return top_artists


def get_spotify_artist_genres(sp, artist):
    """
    Kept for compatibility but NO LONGER USES Spotify API CALLS.
    """

    #This is to get that of the artist's id from the cache.
    artist_id = artist.get("id")
    if artist_id in _artist_genre_cache:
        return _artist_genre_cache[artist_id]

    #This now uses already-provided data instead of API calls
    genres = artist.get("genres", [])

    _artist_genre_cache[artist_id] = genres
    return genres


def get_lastfm_cached(name):

    """
    Get artist tags from Last.fm with caching.
    """

    #This is to get that of the artist's id from the cache.
    if name in _lastfm_cache:
        return _lastfm_cache[name]

    #This tries to get that of an artist's genre(s) by their id.
    # Will send an exception if that said artist's genre(s) cannot be gotten.
    try:
        tags = get_artist_tags(name)
    except Exception as e:
        print(f"[LASTFM ERROR] {name}: {e}")
        tags = []

    #Stores what genres were gotten from an artist.
    _lastfm_cache[name] = tags
    return tags


def get_top_genres(sp, artists):

    """
    Combines Spotify + Last.fm gotten genres from artists and counts frequency.
    """

    print("\nGetting the genres for the artists gotten...")

    #Stores how much that genre has been counted.
    genre_counts = {}

    #For each artist that was gotten and listed....
    for index, artist in enumerate(artists, start=1):

        #Small delay only for Last.fm safety (Spotify no longer needed here)
        time.sleep(0.1)

        #Establish that of their name and id.
        artist_name = artist["name"]

        #This goes through that of the current artist.
        print(f"[{index}/{len(artists)}] Going through: {artist_name}")

        #No Spotify API CALLS HERE ANYMORE
        spotify_raw = artist.get("genres", [])

        #This is to establish the genres gotten from Spotify and add it to a set.
        spotify_genres = set()
        for genre in spotify_raw:
            spotify_genres.add(genre.lower().strip())

        #This is to get that of an artist's genres from Last.fm.
        lastfm_raw = get_lastfm_cached(artist_name)

        #This is to establish the genres gotten from Last.fm and add it to a set.
        lastfm_genres = set()
        for genre in lastfm_raw:
            lastfm_genres.add(genre.lower().strip())

        #This is to combine what genres were gotten from Spotify and Last.fm.
        combined_genres = spotify_genres.union(lastfm_genres)

        #This is to count how many times a specific genre was mentioned.
        for genre in combined_genres:
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

    #Sorts the genres by frequency.
    sorted_genres = dict(
        sorted(
            genre_counts.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

    return sorted_genres


def get_top_tracks(sp, limit=20):

    """
    Fetch user's top tracks from Spotify.
    """

    #This is to get that of the top tracks from the Spotify user.
    results = sp.current_user_top_tracks(
        limit=limit,
        time_range="long_term"
    ).get("items", [])

    #This is where to store the top tracks.
    top_tracks = []

    #For each track that was gotten, get its name and add it.
    for track in results:
        track_name = track.get("name")

        if track_name:
            top_tracks.append(track_name)

    return top_tracks


def build_music_profile(top_artists, top_tracks, top_genres):

    """
    Combines all extracted music data into one structured profile.
    """

    return {
        "top_artists": top_artists,
        "top_tracks": top_tracks,
        "top_genres": top_genres
    }


def clear_internal_caches():

    """
    Clears internal Python caches (Spotify + Last.fm genre/tag cache).
    """
    _artist_genre_cache.clear()
    _lastfm_cache.clear()


def clear_spotify_cache_file():
    
    """
    Removes stored Spotify OAuth token so next login is fully fresh.
    """

    cache_file = ".spotify_cache"

    if os.path.exists(cache_file):
        try:
            os.remove(cache_file)
            print("Spotify cache cleared.")
        except Exception as e:
            print(f"Failed to remove Spotify cache: {e}")