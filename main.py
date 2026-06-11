import streamlit as st

#These are imported to get that of functions from other files. 
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
    create_genre_chart,
    create_top_tracks_chart
)

#How the website is to be established from its layout and website tab's title.
st.set_page_config(
    page_title="PythonMPA - Music Personality Analyzer",
    layout="centered"
)

#Lays out what is expected of the website. 
st.title("Music Personality Analyzer")
st.write("Connect your Spotify account to generate your music personality profile.")


#This is to check that of the user being validated to be logged in for the website.
if "sp" not in st.session_state:
    if st.button("Connect to Spotify"):
        try:
            st.session_state.sp = authenticate_user()
            st.success("Successfully connected to Spotify!")
        except Exception as e:
            st.error(f"Authentication failed: {e}")

#The initial state of the session is that the user has not logged in yet. 
sp = st.session_state.get("sp", None)

#These two functions set that of the cached tracks and artists that were gotten 
# from the Spotify API.
@st.cache_data(ttl=3600)
def cached_top_artists(_sp):
    return get_top_artists(_sp, limit=20)

@st.cache_data(ttl=3600)
def cached_top_tracks(_sp):
    return get_top_tracks(_sp, limit=20)

#If the user was successfully logged in. Else, it would just say that the
# user has to be logged in to get the details gotten from Spotify and Last.fm
if sp:

    st.write("Analyzing your Spotify data...")

    #Spotify API calls for the top artists and tracks. 
    top_artists = cached_top_artists(sp)
    top_tracks = cached_top_tracks(sp)

    #Gets the top genres, which are dependent on getting the artists from Spotify API.
    # From this function, it is a combination of a Spotify and Last.fm API call.
    top_genres = get_top_genres(sp, top_artists)

    #Makes the user profile based on top artists, tracks and genres.
    profile = build_music_profile(
        top_artists,
        top_tracks,
        top_genres
    )

    #Makes the profile for the user's personality based on top artists and genres. 
    personality_profile = generate_personality_profile(
        top_artists,
        top_genres
    )


    #This just shows the full report after the analysis gotten from Spotify and
    # Lastfm APIs. 
    full_profile = {**profile, **personality_profile}
    report = build_report(full_profile)

    st.success("Analysis complete!")
    st.subheader("Your Music Personality Report")

    st.markdown(
        f"### Personality Type\n{full_profile.get('personality', 'Unknown')}"
    )

    st.markdown("### Summary")
    st.write(report["summary"])

    st.markdown("### Trait Explanation")
    st.write(report["trait_explanation"])

    st.markdown("### Charts")

    create_artist_chart(top_artists)
    create_genre_chart(top_genres)
    create_top_tracks_chart(top_tracks)

else:
    st.info("Please connect your Spotify account to begin analysis.")