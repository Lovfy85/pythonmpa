from typing import Dict, List, Any
import streamlit as st


def generate_summary(profile: Dict[str, Any]) -> str:

    """
    This is to make the summary for a personality gotten from the user's calculated 
    artist diversity overall. 
    """

    #The initial values towards that of the profile summary.
    personality = profile.get("personality", "Unknown")
    artist_score = profile.get("artist_score", 0.0)

    #The added parts for the summary to be stored soon.
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
    This is to display the explanations that a user has based on their matched personality.
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


def create_artist_chart(artists: List[Any]) -> None:

    """
    This is to just make a bar chart for the artists listed and how they are
    ranked in a chart.
    """

    if not artists:
        st.write("No artist data available to make the chart overall.")
        return

    st.subheader("Top Artists Breakdown")

    cleaned_artists = [
        a.get("name") if isinstance(a, dict) else str(a)
        for a in artists
    ]

    chart_data = {
        name: rank
        for rank, name in enumerate(cleaned_artists, start=1)
    }

    st.bar_chart(chart_data)


def create_top_tracks_chart(tracks: List[Any]) -> None:

    """
    This is to just make a bar chart for the tracks listed and how they are
    ranked in a chart.
    """

    if not tracks:
        st.write("No track data available to make the chart overall.")
        return

    st.subheader("Top Tracks Breakdown")

    cleaned_tracks = [
        t.get("name") if isinstance(t, dict) else str(t)
        for t in tracks
    ]

    chart_data = {
        name: rank
        for rank, name in enumerate(cleaned_tracks, start=1)
    }

    st.bar_chart(chart_data)


def create_genre_chart(top_genres: Dict[str, int]) -> None:

    """
    This is to just make a bar chart for the genres listed and how they are
    ranked in a chart.
    """

    if not top_genres:
        st.write("No genre data available to make the chart overall.")
        return

    st.subheader("Top Genres Breakdown")
    st.bar_chart(top_genres)


def build_report(profile: Dict[str, Any]) -> Dict[str, Any]:

    """
    This is to make the report summary for the user from their personality
    explained and the charts showing their top artists, genres and tracks.
    """

    summary = generate_summary(profile)
    trait_explanation = generate_trait_explanations(profile)

    artists = profile.get("top_artists", [])
    genres = profile.get("top_genres", {})

    return {
        "summary": summary,
        "trait_explanation": trait_explanation,
        "artists": artists,
        "genres": genres
    }