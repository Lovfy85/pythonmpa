import streamlit as st

#These are imported to get that of functions from other files.
from spotify_client import (
    authenticate_user,
    get_top_artists,
    get_top_tracks,
    get_top_genres,
    build_music_profile,
    clear_internal_caches,
    clear_spotify_cache_file,
    get_overall_personality_profile
)

from report_generator import (
    build_report,
    create_personality_radar_chart,
    create_artist_chart,
    create_genre_chart,
    create_top_tracks_chart
)

#How the website is to be established from its layout and website tab's title.
st.set_page_config(
    page_title="PythonMPA - Music Personality Analyzer",
    layout="centered"
)

#If not logged in right now or the session state begins anew, then, you can present that of the title and
# and the description for website.
if "sp" not in st.session_state or not st.session_state.get("authenticated", False):
    st.title("Music Personality Analyzer")
    st.write("Connect your Spotify account to begin analysis.")

    #If the button is clicked...
    if st.button("Connect to Spotify"):
        try:

            #Gets authentication for user.
            sp = authenticate_user()

            #Has the user authenticated.
            st.session_state.sp = sp
            st.session_state.authenticated = True

            #Immediately jump into app after login.
            st.rerun()

        except Exception as e:
            st.error(f"Authentication failed: {e}")

    #Prevents anything below from running
    st.stop()


#Runs the whole app when logged in.
sp = st.session_state.sp

#Shows two sides by columns
col1, col2 = st.columns([4, 1])

# Get logged-in user's name
user = sp.current_user()
username = user.get("display_name", "Spotify User")

#The left side shows who is logged in as the user.
with col1:
    st.write(f"Logged in as: **{username}**")

with col2:
    if st.button("Logout"):

        # Removes current authenticated user so another user can log in
        st.session_state.pop("sp", None)
        st.session_state.authenticated = False

        # Clears Streamlit cached API responses
        st.cache_data.clear()

        # Clears internal Python caches (LastFM + Spotify genres)
        clear_internal_caches()

        # Clears Spotify OAuth token file
        clear_spotify_cache_file()

        # Force full rerun (fresh state)
        st.rerun()


#If the user was successfully logged in.
if st.session_state.get("authenticated", False):

    st.write("Analyzing your Spotify data...")

    #Spotify API calls for the top artists and tracks.
    top_artists = get_top_artists(sp, limit=20)
    top_tracks = get_top_tracks(sp, limit=20)

    #Gets the top genres
    top_genres = get_top_genres(sp, top_artists)

    #Gets personality profile (NEW SYSTEM)
    personality_profile = get_overall_personality_profile(top_artists)

    #Makes the user profile
    profile = build_music_profile(
        top_artists,
        top_tracks,
        top_genres,
        personality_profile
    )

    #This just shows the full report after the analysis gotten from Spotify and
    # Last.fm APIs.
    report = build_report(profile)

    st.success("Analysis complete!")
    st.subheader("Your Music Personality Report")

    #Show dominant trait safely
    if personality_profile:
        top_trait = max(personality_profile.items(), key=lambda x: x[1])[0]
    else:
        top_trait = "Unknown"

    st.markdown(
        f"### Personality Type\n{top_trait}"
    )

    #Summary dropdown
    with st.expander("Summary", expanded=True):
        st.write(report["summary"])

    #Trait explanation dropdown
    with st.expander("Trait Explanation"):
        st.write(report["trait_explanation"])

    #Personality radar chart dropdown
    with st.expander("Personality Radar Chart"):
        create_personality_radar_chart(profile)

    #Top artists dropdown
    with st.expander("Top Artists"):
        create_artist_chart(top_artists)

    #Top genres dropdown
    with st.expander("Top Genres"):
        create_genre_chart(top_genres)

    #Top tracks dropdown
    with st.expander("Top Tracks"):
        create_top_tracks_chart(top_tracks)

else:
    st.info("Please connect your Spotify account to begin analysis.")