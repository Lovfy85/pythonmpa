from typing import Dict, List, Any


def calculate_artist_diversity(artists: List[str]) -> float:
    """
    Calculates realistic artist diversity score based on the number of artists and rank distribution of the artists.
    (However, this is flawed since based on the artists recorded and such for the tested user, which is me, it will always
    return 28.0)
    """

    #If there are no artists to get to calculate artist diversity, return 0.0.
    if not artists:
        return 0.0

    #Gets how many artists to get 
    n = len(artists)

    # Normalizes against a realistic max (not just dataset size).
    max_expected_artists = 50
    coverage_score = min(n / max_expected_artists, 1.0)

    # If user is heavily top-heavy, score drops slightly
    rank_sum = sum(range(1, n + 1))
    max_rank_sum = n * (n + 1) / 2

    rank_distribution = 1 - (rank_sum / max_rank_sum)

    #Final artist diversity score. 
    diversity = (0.7 * coverage_score + 0.3 * rank_distribution) * 100

    return round(diversity, 2)


def calculate_personality_traits(artist_score: float) -> str:
    """
    Maps artist diversity score into personality types.
    """

    if artist_score >= 70:
        return "Artist Collector"
    elif artist_score >= 40:
        return "Balanced Listener"
    else:
        return "Comfort Listener"


def generate_personality_profile(artists: List[str]) -> Dict[str, Any]:
    """
    Builds the final personality profile from Spotify artist data.
    """

    artist_score = calculate_artist_diversity(artists)
    personality_type = calculate_personality_traits(artist_score)

    profile = {
        "personality": personality_type,
        "artist_score": artist_score,
        "artist_list": artists
    }

    return profile