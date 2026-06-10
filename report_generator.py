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
        "Your music personality has been analyzed based on your Spotify listening habits."
    )

    summary_parts.append(f"You are classified as a '{personality}'")

    summary_parts.append(
        f"and your artist diversity score is {artist_score}."
    )

    if artist_score >= 70:
        summary_parts.append(
            "This suggests you explore a wide variety of artists."
        )
    elif artist_score >= 40:
        summary_parts.append(
            "This suggests you have a balanced listening style."
        )
    else:
        summary_parts.append(
            "This suggests you tend to stick to familiar artists."
        )

    return " ".join(summary_parts)


def generate_trait_explanations(profile: Dict[str, Any]) -> str:
    """
    Makes explanations based on a personality type.
    If not found, return a fallback message.
    """

    personality = profile.get("personality", "Unknown")

    explanations = {
        "Artist Collector": "You explore a wide and diverse range of artists.",
        "Balanced Listener": "You balance familiarity with exploration.",
        "Comfort Listener": "Your taste is stable and consistent over time."
    }

    return explanations.get(
        personality,
        "No explanation available for this personality type."
    )


def create_artist_chart(artists: List[str]) -> None:
    """
    This is to display that of the ranked bar chart of top artists using Streamlit.
    """

    if not artists:
        st.write("No artist data available to make the chart overall.")
        return

    #This is to breakdown that of the top artists gotten. 
    artist_names = list(artists)
    st.subheader("Top Artists Breakdown")
    st.bar_chart(
        data={name: len(artists) - i for i, name in enumerate(artist_names)}
    )


def build_report(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    This is to just make that of the profile overall that was generated.
    """

    summary = generate_summary(profile)
    trait_explanation = generate_trait_explanations(profile)

    artists = profile.get("artist_list", [])

    return {
        "summary": summary,
        "trait_explanation": trait_explanation,
        "artists": artists
    }