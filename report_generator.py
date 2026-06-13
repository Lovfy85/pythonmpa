from typing import Dict, List, Any
import streamlit as st


#Just making each personality label have their own descriptive name. 
PERSONALITY_LABELS = {
    "Creative": "The Sonic Explorer",
    "Introspective": "The Emotional Deep Diver",
    "Energetic": "The Rhythm Driver",
    "Rebellious": "The Sound Rebel",
    "Relaxed": "The Chill Curator"
}


def generate_summary(profile: Dict[str, Any]) -> str:

    """
    This is to make the summary for a personality gotten from the user's calculated 
    artist diversity overall. 
    """

    personality_profile = profile.get("personality_profile", {})
    artist_score = profile.get("artist_score", 0.0)

    #Determine top personality trait + score
    top_trait_key = "Unknown"
    top_trait_score = 0

    if personality_profile:
        top_trait_key, top_trait_score = max(
            personality_profile.items(),
            key=lambda x: x[1]
        )

    #Establish that of the top personality trait overall. 
    top_trait_label = PERSONALITY_LABELS.get(top_trait_key, top_trait_key)

    #To store the summary parts for the summary's paragraph sturcture. 
    summary_parts = []

    summary_parts.append(
        "Your music personality has been analyzed based on the diversity of genres and emotional tags from Spotify and Last.fm."
    )

    summary_parts.append(
        f"Your dominant music personality trait is '{top_trait_label}' ({top_trait_score} points)."
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

    personality_profile = profile.get("personality_profile", {})

    if not personality_profile:
        return "No personality data available."

    #Get top personality trait.
    top_trait_key = max(personality_profile.items(), key=lambda x: x[1])[0]

    explanations = {
        "Creative": (
            "You tend to explore experimental and unconventional sounds. "
            "Your taste leans toward innovation, artistic expression, and unique musical structures."
        ),
        "Introspective": (
            "You gravitate toward emotional, atmospheric, and reflective music. "
            "Your listening habits suggest depth, nostalgia, and emotional awareness."
        ),
        "Energetic": (
            "You prefer high-energy, rhythm-driven music. "
            "Your taste suggests movement, motivation, and upbeat environments."
        ),
        "Rebellious": (
            "You are drawn to aggressive, bold, and high-intensity genres. "
            "Your taste reflects independence and strong emotional expression."
        ),
        "Relaxed": (
            "You enjoy calm, soothing, and low-intensity music. "
            "Your taste suggests relaxation, comfort, and emotional grounding."
        )
    }

    return explanations.get(
        top_trait_key,
        "Your music taste reflects a unique combination of multiple personality traits."
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

    personality_profile = profile.get("personality_profile", {})

    top_trait_key = None
    top_trait_label = None
    top_trait_score = None

    if personality_profile:
        top_trait_key, top_trait_score = max(
            personality_profile.items(),
            key=lambda x: x[1]
        )
        top_trait_label = PERSONALITY_LABELS.get(
            top_trait_key,
            top_trait_key
        )

    return {
        "summary": summary,
        "trait_explanation": trait_explanation,
        "artists": artists,
        "genres": genres,
        "personality_label": top_trait_label,
        "personality_key": top_trait_key,
        "personality_score": top_trait_score
    }