import streamlit as st

#These are imported to get that of functions from other files.
from spotify_client import (
    authenticate_user,
    get_top_artists,
    get_top_tracks,
    get_top_genres,
    build_music_profile,
    clear_internal_caches,
    clear_spotify_cache_file
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

#Makes it so that the user can log in and log out manually. 
col1, col2 = st.columns([4, 1])

with col2:
    if st.button("Logout"):

        #Removes current authenticated user so another user can log in
        st.session_state.pop("sp", None)
        st.session_state.authenticated = False

        #Clears Streamlit cached API responses
        st.cache_data.clear()

        #Clears internal Python caches (LastFM + Spotify genres)
        clear_internal_caches()

        #Clears Spotify OAuth token file
        clear_spotify_cache_file()

        #Force full rerun (fresh state)
        st.rerun()


#These two functions set that of the cached tracks and artists that were gotten
# from the Spotify API.
@st.cache_data(ttl=3600)
def cached_top_artists(token):
    sp = st.session_state.sp
    return get_top_artists(sp, limit=20)

@st.cache_data(ttl=3600)
def cached_top_tracks(token):
    sp = st.session_state.sp
    return get_top_tracks(sp, limit=20)


#If the user was successfully logged in.
if st.session_state.get("authenticated", False):

    st.write("Analyzing your Spotify data...")

    #Spotify API calls for the top artists and tracks.
    top_artists = cached_top_artists("token")
    top_tracks = cached_top_tracks("token")

    #Gets the top genres
    top_genres = get_top_genres(sp, top_artists)

    #Makes the user profile
    profile = build_music_profile(
        top_artists,
        top_tracks,
        top_genres
    )

    #Personality profile
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