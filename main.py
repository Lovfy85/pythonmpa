import streamlit as st

#This is to get that of the functions seen in other files.
from spotify_client import (
    authenticate_user,
    get_top_artists,
    get_top_tracks,
    get_top_genres,
    build_music_profile
)
from analyzer import generate_personality_profile
from report_generator import (
    build_report,
    create_artist_chart,
    create_genre_chart
)

#Sets that of the configuration towards that of the website's tab title and element layout.
st.set_page_config(
    page_title="PythonMPA - Music Personality Analyzer",
    layout="centered"
)

#Title of the website inside.
st.title("Music Personality Analyzer")

#This is to connect that of the Spotify account in the website.
st.write("Connect your Spotify account to generate your music personality profile.")
sp = None

if "sp" not in st.session_state:

    if st.button("Connect to Spotify"):
        try:
            st.session_state.sp = authenticate_user()
            st.success("Successfully connected to Spotify!")
        except Exception as e:
            st.error(f"Authentication failed: {e}")

# retrieve session connection
sp = st.session_state.get("sp", None)


if sp:

    st.write("Analyzing your Spotify data...")

    #Get raw Spotify data
    top_artists = get_top_artists(sp, limit=20)
    top_tracks = get_top_tracks(sp, limit=20)
    top_genres = get_top_genres(sp, limit=20)

    #Build base music profile
    profile = build_music_profile(
        top_artists,
        top_tracks,
        top_genres
    )

    # Personality analysis (single source of truth)
    personality_profile = generate_personality_profile(
        top_artists,
        top_genres
    )

    #Merge everything into final profile
    full_profile = {**profile, **personality_profile}

    #Generate report
    report = build_report(full_profile)

    st.success("Analysis complete!")

    st.subheader("Your Music Personality Report")
    st.markdown(f"### Personality Type\n{full_profile.get('personality', 'Unknown')}")

    st.markdown("### Summary")
    st.write(report["summary"])

    st.markdown("### Trait Explanation")
    st.write(report["trait_explanation"])

    st.markdown("### Charts")

    #Artist chart
    create_artist_chart(top_artists)

    #Genre chart (NEW)
    create_genre_chart(top_genres)

    st.markdown("### Top Tracks")

    #If there are existing top tracks overall.
    if top_tracks:

        #Starts the first track at 1.
        track_number = 1

        #Towards each track in the top tracks...
        for track in top_tracks:

            #This is to make sure that if for whatever reason a track cannot be gotten, just execute the if-condition
            if isinstance(track, dict):
                track_name = track.get(
                    "name",
                    "Unknown Track"
                )

            #If there is an existing track, get the name of the current track.
            else:
                track_name = track

            #Writes that of the track number and name unto the website.
            st.write(
                f"{track_number}. {track_name}"
            )

            #Move unto the next one.
            track_number += 1

    #If there is not, then, execute this message.
    else:
        st.write(
            "No track data available."
        )