import google.generativeai as genai
import requests
import streamlit as st
import json, re

# Load API keys from Streamlit secrets
GEMINI_API_KEY = st.secrets["apis"]["gemini_key"]
YOUTUBE_API_KEY = st.secrets["apis"]["youtube_key"]
WATCHMODE_API_KEY = st.secrets["apis"]["watchmode_key"]

genai.configure(api_key=GEMINI_API_KEY)

KNOWN_MOODS = [
    "Happy", "Sad", "Anxious", "Angry", "Confused", "Grateful", "Lonely",
    "Excited", "Burned Out", "Motivated", "Tired", "Overwhelmed", "Calm",
    "Frustrated", "Hopeful", "Depressed", "Joyful", "Peaceful", "Heartbroken"
]

def detect_mood_and_recommend(user_input):
    prompt = f"""
The user says: "{user_input}"

Your tasks:
1. From the following list of moods, pick the ONE best matching the user's emotional state:
{', '.join(KNOWN_MOODS)}

2. Recommend one music artist or playlist for this mood, preferably Bollywood.

3. Suggest one movie title appropriate for this emotional state.

4. Write a warm, empathetic, comforting paragraph-type therapy-style message including how to proceed further.

Return your answer in **exact** JSON format as:

{{
  "mood": "...",
  "music": "...",
  "movie": "...",
  "therapy": "..."
}}
"""
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    try:
        json_like = re.search(r'\{.*\}', response.text, re.DOTALL).group()
        return json.loads(json_like)
    except Exception as e:
        print("Gemini Parsing Error:", e)
        return {
            "mood": "Confused",
            "music": "Try listening to calming piano music or lo-fi beats.",
            "movie": "Inside Out – a thoughtful movie about emotions.",
            "therapy": "It's okay to feel confused. You're not alone in this. Take a small step forward—clarity follows action."
        }

def get_youtube_music_video(music):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": music + " song",
        "key": YOUTUBE_API_KEY,
        "type": "video",
        "maxResults": 1
    }
    res = requests.get(url, params=params).json()
    if res.get("items"):
        video = res['items'][0]
        return (
            video['snippet']['title'],
            f"https://www.youtube.com/watch?v={video['id']['videoId']}",
            video['snippet']['thumbnails']['high']['url']
        )
    return None, None, None

def get_movie_streaming_info(movie):
    try:
        search_url = "https://api.watchmode.com/v1/search/"
        params = {
            "apiKey": WATCHMODE_API_KEY,
            "search_value": movie,
            "search_field": "name",
            "search_type": 1
        }
        search_response = requests.get(search_url, params=params).json()

        if not search_response.get("title_results"):
            return None

        movie_id = search_response["title_results"][0]["id"]
        sources_url = f"https://api.watchmode.com/v1/title/{movie_id}/sources/"
        source_params = {"apiKey": WATCHMODE_API_KEY}
        sources = requests.get(sources_url, params=source_params).json()

        platforms = []
        seen = set()

        for src in sources:
            name = src["name"]
            url = src.get("web_url", "")
            access_type = src["type"]
            key = (name, url, access_type)
            if key not in seen:
                seen.add(key)
                platforms.append((f"{name} ({access_type})", url))

        return platforms

    except Exception as e:
        print("Error getting streaming info:", e)
        return None
