# from tmdb import route, schema
import os

# # Initialize TMDB
# tmdb = route.Base()
# tmdb.key = os.getenv("TMDB_API_KEY")


YOUTUBE_API_KEY="AIzaSyDccAQACPXk5uMb-ctKRJbxwwTEIEhpJOc"

def search_youtube_music(mood):
    api_key = YOUTUBE_API_KEY
    search_url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": f"{mood} mood music",
        "key": api_key,
        "type": "video",
        "maxResults": 1
    }

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        results = response.json()

        if "items" in results and results["items"]:
            video_id = results["items"][0]["id"]["videoId"]
            title = results["items"][0]["snippet"]["title"]
            thumbnail = results["items"][0]["snippet"]["thumbnails"]["high"]["url"]
            return {
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "title": title,
                "thumbnail": thumbnail
            }

    except Exception as e:
        print("YouTube API error:", e)

    return None

import requests
import streamlit as st

WATCHMODE_API_KEY = "ZOIyNaBP6s3lh5Hadfdp4UEiDjTv9A4CwN9x7pJs"

def search_movie_watchmode(title):
    # Step 1: Search for movie ID
    search_url = "https://api.watchmode.com/v1/search/"
    params = {
        "apiKey": WATCHMODE_API_KEY,
        "search_field": "title",
        "search_value": title,
        "types": "movie"
    }
    res = requests.get(search_url, params=params).json()
    if not res["title_results"]:
        return None
    
    movie = res["title_results"][0]
    movie_id = movie["id"]

    # Step 2: Get streaming availability
    details_url = f"https://api.watchmode.com/v1/title/{movie_id}/details/"
    sources_url = f"https://api.watchmode.com/v1/title/{movie_id}/sources/"

    details = requests.get(details_url, params={"apiKey": WATCHMODE_API_KEY}).json()
    sources = requests.get(sources_url, params={"apiKey": WATCHMODE_API_KEY}).json()

    return {
        "title": movie["name"],
        "year": movie.get("year"),
        "poster": details.get("poster"),
        "overview": details.get("plot_overview"),
        "sources": sources
    }
