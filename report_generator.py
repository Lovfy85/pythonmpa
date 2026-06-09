from typing import Dict, List, Any
import streamlit as st

def generate_summary(profile: Dict[str, Any]) -> str:

    """
    This is to create that of the paragraph summary structure for the user's personality profile.
    """

    #This is to get that of the initial personality, genre score and artist score.
    personality = profile.get("personality", "Unknown")
    genre_score = profile.get("genre_score", 0.0)
    artist_score = profile.get("artist_score", 0.0)

    #This is to store soon that of the things included in the paragraph summary structure.
    summary_parts = []
    
    summary_parts.append("Your music personality has been analuzed based on your Spotify listening habits.")
    summary_parts.append(f"You are classified as a '{personality}'")

    summary_parts.append(
        f"Your genre diveristy score is {genre_score}, "
        f"and your artist diversity score is {artist_score}."
    )

    #These are then that of interpreting what the scores are about.
    if genre_score > 60 and artist_score > 60:
        summary_parts.append(
            "This suggests you explore a wide variety of both genres and artists."
        )

    elif genre_score > 60:
        summary_parts.append(
            "This suggest you explore many genres, but tend to stick to familiar artists."
        )

    elif artist_score > 60:
        summary_parts.append(
            "This suggests you explore many artists, but stay within a smaller set of genres."
        )

    else: 
        summary_parts.append(
            "This suggests you prefer familiar music patterns and repeat listening habits."
        )

    #This then makes the whole pargraph.
    return " ".join(summary_parts)


def generate_trait_explanations(profile: Dict[str, Any]) -> str: 

    """
    Makes explanations based on a personality type. If not gotten a personality for whatever reason, 
    just return that it does not have an explanation.
    """

    personality = profile.get("personality", "Unknown")

    explanations = {
        "Musical Explorer": (
            "You enjoy discovering both new artists and new genres."
            "Your listening habits show high curiosity and variety."
        ),

        "Genre Adventurer": (
            "You explore many genres, but tend to return to familiar artists."
            "You like variety in sound but comfort in voices you trust."
        ),

        "Artist Collector": (
            "You follow a wide range of artists, but tend to stay within a few genres."
            "You value artist identity over genre exploration."
        ),

        "Comfort Listener": (
            "You prefer familiar music and repeat listening patterns."
            "Your taste is stable and consistent over time."
        )
    }

    return explanations.get(
        personality,
        "No explanation available for this personality type."
    )


def create_genre_chart(genres: Dict[str, int]) -> None:

    """
    This is to display that of the genre distribution bar chart using Streamlit.
    """

    if not genres:
        st.write("No genre data available to make the chart overall.")
        return
    
    #This is to make that of the dictionary passed as an argument from 'genres' to lists for Streamlit.
    genre_names = []
    genre_counts = []

    #Then, for each of the genres and their counts listed, add it to their respective lists for Streamlit.
    for genre, count in genres.items():
        genre_names.append(genre)
        genre_counts.append(count)

    #This is to display that of the chart overall.
    st.subheader("Top Genres Breakdown")
    st.bar_chart(
        data = {
            "Genre": genre_names, 
            "Count": genre_counts
        }
    )


def create_artist_chart(artists: List[str]) -> None:

    """
    This is to display that of the ranked bar chart of top artists using Streamlit.
    """

    if not artists:
        st.write("No artist data available to make the chart overall.")
        return
    
    #This is to make that of the list passed as an argument from 'artists' to lists for Streamlit.
    artist_names = []
    artist_scores = []

    #This is to get the maximum rank of artists.
    rank_score = len(artists)

    #As we getting the artists, add their names and scores to their respective lists.
    for artist in artists:
        artist_names.append(artist)
        artist_scores.append(rank_score)

        rank_score -= 1 #decrease score per rank

    #This is to display the chart overall. 
    st.subheader("Top Artists Breakdown")
    st.bar_chart(
        data = {
            "Artist": artist_names,
            "Score": artist_scores
        }
    )


def build_report(profile: Dict[str, Any]) -> Dict[str, Any]:

    """
    This is to just make that of the profile overall that was genreated.
    """

    summary = generate_summary(profile)
    trait_explanation = generate_trait_explanations(profile)

    genres = profile.get("genre_breakdown", {})
    artists = profile.get("artist_list", [])

    return {
        "summary": summary,
        "trait_explanation": trait_explanation,
        "genres": genres,
        "artists": artists
    }