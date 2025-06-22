import google.generativeai as genai
import requests
import streamlit as st
import json, re
from datetime import datetime

# Load API keys from Streamlit secrets
gemini_api = st.secrets["GEMINI_API_KEY"]
youtube_api = st.secrets["YOUTUBE_API_KEY"]
watchmode_api= st.secrets["WATCHMODE_API_KEY"]

genai.configure(api_key=gemini_api)

# Define known moods
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
            "music": "Try listening to some calming piano music or lo-fi beats.",
            "movie": "Inside Out – a thoughtful movie about emotions.",
            "therapy": "It's okay to feel confused. You're not alone in this. Take a small step forward, even if it’s unclear — clarity often follows action."
        }

def get_youtube_music_video(music):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": music + " song",
        "key": youtube_api,
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
        search_params = {
            "apiKey": watchmode_api,
            "search_value": movie,
            "search_field": "name",
            "search_type": 1
        }
        search_response = requests.get(search_url, params=search_params).json()

        if not search_response.get("title_results"):
            print("❌ No title results found.")
            return None

        movie_id = search_response["title_results"][0]["id"]

        sources_url = f"https://api.watchmode.com/v1/title/{movie_id}/sources/"
        sources = requests.get(sources_url, params={"apiKey": watchmode_api}).json()

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
        print("⚠️ Error in movie streaming info:", e)
        return None
