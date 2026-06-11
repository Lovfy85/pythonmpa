import requests
from config import LASTFM_API_KEY

#Base URL for all Last.fm API requests.
BASE_URL = "http://ws.audioscrobbler.com/2.0/"


def get_artist_tags(artist_name, limit=5):

    """
    Fetch label tags for an artist from Last.fm. These label tags from
    an artist is to get that of the genres they are in. 
    """

    #The parameters here are to be used in order to get the tags we want
    # in a .json response format.
    params = {
        "method": "artist.gettoptags",
        "artist": artist_name,
        "api_key": LASTFM_API_KEY,
        "format": "json"
    }

    #This is to get that of the artist's label tags with the request 
    # structured from the parameters stated. If it works, it should
    # get each genre from each artist. If not, return an exception.
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        tags = data.get("toptags", {}).get("tag", [])

        #To hold only genre names.
        genres = []

        #Restrict how many tags we process
        limited_tags = tags[:limit]

        #loop through each tag dictionary returned by Last.fm
        for tag in limited_tags:

            #Ensure the key exists to prevent crashing.
            if "name" in tag:

                #Get the genre's name
                genre_name = tag["name"]

                #Store it in the genres list.
                genres.append(genre_name)

        return genres

    except Exception as e:
        print(f"There seems to be an error for getting {artist_name}: {e}")
        return []