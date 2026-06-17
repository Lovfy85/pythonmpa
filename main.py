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
    page_title="Spotify Personality Analyzer",
    layout="wide"
)

#Loads CSS styling from separate file.
with open("styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

#Just to show that of the website when first booted up. 
if "sp" not in st.session_state or not st.session_state.get("authenticated", False):

    #Showcasing what the website is all about. 
    st.markdown("""
    <div class="landing-header">
        <div class="landing-title">🎧 Spotify Personality Analyzer 🎧</div>
        <div class="landing-subtitle">
            Discover what your Spotify taste says about your personality.
        </div>
    </div>
    """, unsafe_allow_html=True)

    #Divider for visual separation
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    #Section title for features
    st.markdown("## What the website's features are: ")

    #This is the feature section showcasing what types of features there are overall that can be seen
    # when logging in the website. 
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎵</div>
            <h3>Taste Analysis</h3>
            <p>Analyzes your top artists, tracks, and genres you have listened throughout the years to understand your listening habits.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <h3>Personality Profile</h3>
            <p>Your overall music taste connects to a personality trait and generates an explanation behind it.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>Visual Insights</h3>
            <p>Charts to show who your top artists, genres and tracks are as well as what personality you are closest to.</p>
        </div>
        """, unsafe_allow_html=True)

    #Spacing divider
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    #CTA section (call to action)
    st.markdown("""
    <div class="cta-section">
        <div class="cta-title">Ready to discover your music identity?</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Connect to Spotify", use_container_width=True):
        try:

            #Gets authentication for user.
            sp = authenticate_user()

            #Stores authenticated session
            st.session_state.sp = sp
            st.session_state.authenticated = True

            #Immediately jump into app after login.
            st.rerun()

        except Exception as e:
            st.error(f"Authentication failed: {e}")

    #Prevents anything below from running
    st.stop()

#Establishes for the user to log in the website. 
sp = st.session_state.sp

#Gets information about the logged-in user.
user = sp.current_user()
username = user.get("display_name", "Spotify User")

#Gets the user's Spotify profile picture if one exists.
images = user.get("images", [])
profile_pic = images[0]["url"] if images else None


#Creates the profile header and logout section.
with st.container():

    col1, col2 = st.columns([5, 1])

    with col1:
        header_col1, header_col2 = st.columns([1, 5])

        with header_col1:
            if profile_pic:
                st.image(profile_pic, width=160)

        with header_col2:
            st.markdown(
                f"""
                <div class="user-card">
                    <div class="user-name-line">
                        🎵 Logged in as: <span class="username">{username}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col2:

        st.write("")
        st.write("")

        if st.button("🚪 Logout", use_container_width=True):

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


#Just goes over the analysis. 
if st.session_state.get("authenticated", False):

    with st.status("🎧 Analyzing your music identity...", expanded=True) as status:

        st.write("Fetching top artists...")
        top_artists = get_top_artists(sp, limit=20)

        st.write("Fetching top tracks...")
        top_tracks = get_top_tracks(sp, limit=20)

        st.write("Analyzing genres...")
        top_genres = get_top_genres(sp, top_artists)

        st.write("Building personality profile...")
        personality_profile = get_overall_personality_profile(top_artists)

        st.write("Generating full music profile...")
        profile = build_music_profile(
            top_artists,
            top_tracks,
            top_genres,
            personality_profile
        )

        st.write("Writing report...")
        report = build_report(profile)

        status.update(label="Analysis complete!", state="complete")


    st.markdown("## Your Music Personality Report")

    #Show dominant trait safely
    if personality_profile:
        top_trait = max(personality_profile.items(), key=lambda x: x[1])[0]
    else:
        top_trait = "Unknown"

    #Highlight card (main result)
    st.markdown(f"""
    <div class="highlight-card">
        <div class="highlight-label">Your Dominant Personality</div>
        <div class="highlight-value">{top_trait}</div>
    </div>
    """, unsafe_allow_html=True)


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