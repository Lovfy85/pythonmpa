from typing import Dict, List, Any
import streamlit as st


def generate_summary(profile: Dict[str, Any]) -> str:
    
    """
    This is to create that of the paragraph summary structure for the user's personality profile.
    """

    personality = profile.get("personality", "Unknown")
    artist_score = profile.get("artist_score", 0.0)

    summary_parts = []

    summary_parts.append(
        "Your music personality has been analyzed based on the diversity of genres represented by the artists you listen to most frequently."
    )

    summary_parts.append(
        f"You are classified as an '{personality}' listener with a diversity score of {artist_score}."
    )

    if artist_score >= 70:
        summary_parts.append(
            "Your listening habits suggest a strong tendency toward exploring a wide variety of musical styles and artist backgrounds."
        )

    elif artist_score >= 40:
        summary_parts.append(
            "Your listening habits suggest a balance between familiar favorites and discovering new musical influences."
        )

    else:
        summary_parts.append(
            "Your listening habits suggest a focused musical identity centered around genres and artists that consistently resonate with you."
        )

    return " ".join(summary_parts)


def generate_trait_explanations(profile: Dict[str, Any]) -> str:

    """
    Makes explanations based on a personality type.
    If not found, return a fallback message.
    """

    personality = profile.get("personality", "Unknown")

    explanations = {
        "Artist Collector": (
            "You regularly explore artists from a broad range of genres. "
            "Your listening patterns suggest curiosity, openness, and a willingness "
            "to discover new musical experiences."
        ),

        "Balanced Listener": (
            "You maintain a healthy balance between your favorite artists and new discoveries. "
            "You enjoy familiarity while remaining open to different sounds and styles."
        ),

        "Comfort Listener": (
            "You have a strong connection to the music you enjoy most. "
            "Your listening habits show consistency and a deep appreciation "
            "for particular artists and genres."
        )
    }

    return explanations.get(
        personality,
        "No explanation available for this personality type."
    )



def create_artist_chart(artists: List[str]) -> None:

    """
    This displays the ranked list of top artists using Streamlit.
    """

    if not artists:
        st.write("No artist data available to make the chart overall.")
        return

    st.subheader("Top Artists Breakdown")

    # Proper ranking instead of fake weighted values
    chart_data = {
        artist: rank
        for rank, artist in enumerate(artists, start=1)
    }

    st.bar_chart(chart_data)


def create_genre_chart(top_genres: Dict[str, int]) -> None:

    """
    This displays the user's top genres based on frequency.
    """

    if not top_genres:
        st.write("No genre data available to make the chart overall.")
        return

    st.subheader("Top Genres Breakdown")

    # Direct frequency mapping from Spotify-derived data
    st.bar_chart(top_genres)


def build_report(profile: Dict[str, Any]) -> Dict[str, Any]:

    """
    This is to just make that of the profile overall that was generated.
    """

    summary = generate_summary(profile)

    trait_explanation = generate_trait_explanations(profile)

    artists = profile.get("artist_list", [])

    genres = profile.get("top_genres", {})

    return {
        "summary": summary,
        "trait_explanation": trait_explanation,
        "artists": artists,
        "genres": genres
    }