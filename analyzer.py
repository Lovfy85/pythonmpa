from typing import Dict, Any


def calculate_artist_diversity(top_genres: Dict[str, int]) -> float:

    """
    Calculates diversity based on how evenly the user's
    listening habits are spread across genres.

    Higher scores indicate broader musical exploration.
    Lower scores indicate stronger focus on a smaller
    set of genres.
    """

    if not top_genres:
        return 0.0

    total = sum(top_genres.values())

    if total == 0:
        return 0.0

    diversity_score = 0.0

    for count in top_genres.values():
        proportion = count / total

        # Penalize genres that dominate listening habits.
        diversity_score += (1 - proportion)

    diversity_score = (diversity_score / len(top_genres)) * 100

    return round(diversity_score, 2)


def calculate_personality_traits(artist_score: float) -> str:

    """
    Maps diversity score into personality categories.
    """

    if artist_score >= 75:
        return "Artist Collector"

    elif artist_score >= 50:
        return "Balanced Listener"

    else:
        return "Comfort Listener"


def generate_personality_profile(artists, top_genres: Dict[str, int]) -> Dict[str, Any]:

    """
    Builds the final personality profile.
    """

    artist_score = calculate_artist_diversity(top_genres)

    personality_type = calculate_personality_traits(artist_score)

    if personality_type == "Artist Collector":

        summary = (
            "Your listening habits suggest a highly exploratory "
            "approach to music. You regularly engage with artists "
            "from many different genre backgrounds, demonstrating "
            "curiosity and openness to discovering new sounds."
        )

    elif personality_type == "Balanced Listener":

        summary = (
            "Your music taste balances familiarity and exploration. "
            "While you have clear preferences, you also branch out "
            "into different styles and artists when something "
            "captures your interest."
        )

    else:

        summary = (
            "Your listening habits show a focused musical identity. "
            "You tend to develop strong connections with particular "
            "genres and artists, allowing you to build a deep "
            "appreciation for the music that resonates most with you."
        )

    profile = {
        "personality": personality_type,
        "artist_score": artist_score,
        "artist_list": artists,
        "top_genres": top_genres,
        "summary": summary
    }

    return profile