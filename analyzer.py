from typing import Dict, List, Any

#With these type of functions like this as its function header, 
# it is to make explicit traits of what it is to be an argument put in and what is expected to return. 
def calculate_genre_diversity(genres: Dict[str, int]) -> float:
    
    """
    Calculates how varied the user's genre taste is.
    """

    #This is to check if there was an empty input, to which will return 0.0.
    if genres is None or len(genres) == 0:
        return 0.0
    
    #This is to go over that of the unique genres seen overall. 
    unique_genre_count = 0
    for _ in genres: 
        unique_genre_count += 1

    #This is to get that of the total genre mentions overall.
    total_genre_mentions = 0
    for count in genres.values():
        total_genre_mentions += count

    #This is to avoid that of division errors.
    if total_genre_mentions == 0:
        return 0.0
    
    #This is to make the ratio based on unique genres counted divided by the 
    # total genre mentions.
    ratio = unique_genre_count / total_genre_mentions

    #This is to convert the ratio's value into a percentage score.
    score = ratio * 100

    #Returns the score as a double value by 2 decimals. 
    return round(score, 2)


def calculate_artist_diversity(artists: List[str]) -> float:

    """
    Calculates that of the user's diverse taste in artists. 
    """

    #This is to check if there was an empty input, to which will return 0.0.
    if artists is None or len(artists) == 0:
        return 0.0
    
    #This is to over that of the total artists mentioned overall.
    total_artists = 0
    for artist in artists: 
        total_artists += 1

    #This is to get that of the unique artists overall.
    unique_artist_set = set()

    #For each artist gotten, add them to the set. 
    for artist in artists:
        unique_artist_set.add(artist)

    #This is to go over that of the unique artists overall. 
    unique_artist_count = 0
    for _ in unique_artist_set: 
        unique_artist_count += 1

    #This is to avoid that of division errors.
    if total_artists == 0:
        return 0.0
    
    #This is to make the ratio based on the count of the unique artist count divided
    # by the total artists mentioned. 
    ratio = unique_artist_count / total_artists

    #This is to convert ratio's value into a percentage score.
    score = ratio*100

    #Returns the score as a double value by 2 decimals.
    return round(score, 2)


def calculate_personality_traits(genre_score: float, artist_score: float) -> str:

    """
    This is to match whatever personality trait the user has based on that of the user's
    diversity scores.
    """

    #This is to establish the threshold that will be the determiner what the user's personality
    # trait will be based on the user's scores. 
    HIGH_THRESHOLD = 60

    #Checks if that of the genre score will be more than that of the threshold.
    if genre_score >= HIGH_THRESHOLD:
        if artist_score >= HIGH_THRESHOLD:
            return "Musical Explorer"
        else:
            return "Genre Adventurer"
    else:
        if artist_score >= HIGH_THRESHOLD:  
            return "Artist Collector"
        else: 
            return "Comfort Listener"
        

def generate_personality_profile(genres: Dict[str, int], artists: List[str]) -> Dict[str, Any]:

    """
    This is to make that of the personality profile from the Spotify data.
    """

    #This is to get that of the genre score.
    genre_score = calculate_genre_diversity(genres)

    #This is to get that of the artist score.
    artist_score = calculate_artist_diversity(artists)

    #This is to determine that of the personality type.
    personality_type = calculate_personality_traits(
        genre_score, 
        artist_score
    )

    #Builds that of the structure for the profile.
    profile = {}
    profile["personality"] = personality_type
    profile["genre_score"]  = genre_score
    profile["artist_score"] = artist_score
    profile["genre_breakdown"] = genres
    profile["artist_list"] = artists

    return profile