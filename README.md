# Music Personality Analyzer
A web-based music analytics application that analyzes a user's Spotify listening habits to generate a personalized music personality profile. Using data from the Spotify Web API and Last.fm API, the application provides insights into listening behavior through interactive visualizations, personality analysis, genre breakdowns, and a downloadable PDF report.

--- 
## Features
- Secure Spotify OAuth authentication
- Retrieves and analyzes a user's top artists, tracks, and genres
- Hybrid genre detection using Spotify and Last.fm
- Generates a personalized music personality profile based on listening habits
- Interactive charts and visualizations
- Personality radar chart
- Downloadable PDF personality report
- API response caching to improve performance and reduce unnecessary API requests

--- 
## Technologies Used
### Language
- Python

### Libraries & Frameworks
- Streamlit
- Spotipy
- Plotly
- Pandas
- ReportLab
- Requests
- python-dotenv

### APIs
- Spotify Web API
- Last.fm API

---
## Prerequisites
Before running the application, ensure you have:
- Python 3.11 or later
- A Spotify Developer account
- A Last.fm API key from making a Last.fm account

---
## Installation

### 1. Clone the repository

```
git clone https://github.com/Lovfy85/pythonmpa.git cd MusicPersonalityAnalyzer
```

### 2. (Recommended) Create a virtual environment

**Windows**

```
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the required dependencies

```
pip install -r requirements.txt
```

---

## API Setup
### Spotify
1. Visit the Spotify Developer Dashboard.
2. Create a new application.
3. Copy your **Client ID** and **Client Secret**.
4. Add the redirect URI configured in the project (for example):

```
http://localhost:8501/callback
```

### Last.fm
1. Create a Last.fm developer account.
2. Generate an API key.

---
## Environment Variables
Create a `.env` file in the project's root directory and add:

```
SPOTIPY_CLIENT_ID=YOUR_CLIENT_ID
SPOTIPY_CLIENT_SECRET=YOUR_CLIENT_SECRET
SPOTIPY_REDIRECT_URI=http://localhost:8501/callback

LASTFM_API_KEY=YOUR_LASTFM_API_KEY
```
Replace each placeholder with your own API credentials.

---
## Running the Application

Start the application with:

```
streamlit run main.py
```

If the browser does not open automatically, visit:

```
http://localhost:8501
```

---
## Using the Application

1. Launch the application.
2. Log in with your Spotify account.
3. Authorize access to your Spotify data.
4. Wait while your listening history is analyzed.
5. Explore your personalized dashboard, including:
    - Top Artists
    - Top Tracks
    - Genre Breakdown
    - Music Personality Profile
    - Personality Radar Chart
    - Interactive Visualizations
6. Download your personalized PDF report if you want to. 

---
## Project Structure

```
MusicPersonalityAnalyzer/
├── .gitignore
├── analyzer.py
├── config.py
├── lastfm_client.py
├── main.py
├── README.md
├── report_generator.py
├── spotify_client.py
└── styles.css
```

---
## Dependencies

Install all required packages with:

```
pip install -r requirements.txt
```

The project uses the following Python libraries:

- streamlit
- spotipy
- plotly
- pandas
- reportlab
- python-dotenv
- requests

---
## Author

Developed by **Cedar Ancheta** as a personal portfolio project demonstrating API integration, data analysis, interactive data visualization, and full-stack application development using Python.

License
Copyright (c) 2026 Cedar Ancheta
All rights reserved. 
