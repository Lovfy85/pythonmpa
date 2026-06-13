import requests
from config import LASTFM_API_KEY

#Base URL for all Last.fm API requests.
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

#Maps Last.fm tags to personality traits. Will include more specific genres towards
# a correlated personality tag soon. 
PERSONALITY_TAGS = {
    "Creative": [
        "experimental",
        "art pop",
        "avant-garde",
        "progressive",
        "psychedelic"
    ],

    "Introspective": [
        "melancholic",
        "sad",
        "ambient",
        "dream pop",
        "nostalgic"
    ],

    "Energetic": [
        "dance",
        "electronic",
        "workout",
        "party",
        "house"
    ],

    "Rebellious": [
        "punk",
        "grunge",
        "metal",
        "hardcore"
    ],

    "Relaxed": [
        "chill",
        "lofi",
        "acoustic",
        "folk"
    ]
}


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
        print(f"Getting tags for artist: {artist_name}")

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        tags = data.get("toptags", {}).get("tag", [])

        print(f"Retrieved {len(tags)} tags for {artist_name}")

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

        print(f"Top tags for {artist_name}: {genres}")

        return genres

    except Exception as e:
        print(f"There seems to be an error for getting {artist_name}: {e}")
        return []


def get_artist_tag_data(artist_name, limit=20):

    """
    Fetch tags that are mostly associated towards the artist with how much weight
    those tags are overall.
    """

    print(f"Getting weighted tag data for {artist_name}")

    params = {
        "method": "artist.gettoptags",
        "artist": artist_name,
        "api_key": LASTFM_API_KEY,
        "format": "json"
    }

    
    try:

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        tags = data.get("toptags", {}).get("tag", [])

        limited_tags = tags[:limit]

        print(
            f"Retrieved {len(limited_tags)} weighted tags "
            f"for {artist_name}"
        )

        return limited_tags

    except Exception as e:
        print(
            f"There seems to be an error for getting tag data "
            f"for {artist_name}: {e}"
        )
        return []


def get_artist_personality_scores(artist_name, limit=20):

    """
    Make the tags gotten to be converted into personality scores for that artist. 
    It is to establish them towards a personality.
    """

    print(
        f"Calculating personality scores "
        f"for {artist_name}"
    )

    tag_data = get_artist_tag_data(artist_name, limit)

    personality_scores = {}

    #Initialize all traits to zero.
    for trait in PERSONALITY_TAGS:
        personality_scores[trait] = 0

    #For each gotten tag by their name...
    for tag in tag_data:

        tag_name = tag.get("name", "").lower()

        #Counts that of the tag's weight overall. However, 
        # if not counted, set it to 1.
        try:
            tag_weight = int(tag.get("count", 1))
        except:
            tag_weight = 1

        #With the tag gotten, display how much its weight is. 
        print(
            f"Processing tag "
            f"'{tag_name}' (weight={tag_weight})"
        )

        #For each trait tag said in personality tags...
        for trait, associated_tags in PERSONALITY_TAGS.items():

            #If there is a tag name that can be seen in personality tags,
            # add the tag weight onto that personality score towards that 
            # specific trait. 
            if tag_name in associated_tags:

                personality_scores[trait] += tag_weight

                #Display the matched tag with the personality trait with its weight score. 
                print(
                    f"Matched tag "
                    f"'{tag_name}' -> {trait} "
                    f"(+{tag_weight})"
                )

    #This displays that of an artist's personality score based on the weight of their
    # tags they are associated with to which those tags are to connect with what personality
    # tag listed in the personality collection. 
    print(
        f"Final scores for "
        f"{artist_name}: {personality_scores}"
    )

    return personality_scores


def get_dominant_personality_traits(artist_name, limit=20):

    """
    Returns the strongest personality traits for an artist.
    """

    print(
        f"Determining dominant traits "
        f"for {artist_name}"
    )

    personality_scores = get_artist_personality_scores(
        artist_name,
        limit
    )

    sorted_traits = sorted(
        personality_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    print(
        f"Ranked traits for "
        f"{artist_name}: {sorted_traits}"
    )

    return sorted_traits