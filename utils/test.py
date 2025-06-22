import requests

WATCHMODE_API_KEY = "ZOIyNaBP6s3lh5Hadfdp4UEiDjTv9A4CwN9x7pJs"
movie_title = "Eternal Sunshine of the Spotless Mind"

# Fixed search with search_field
search_url = "https://api.watchmode.com/v1/search/"
params = {
    "apiKey": WATCHMODE_API_KEY,
    "search_value": movie_title,
    "search_field": "name",     # ✅ This was missing earlier
    "search_type": 1             # 1 = movie
}
search_response = requests.get(search_url, params=params).json()
print("🔎 Search Response:")
print(search_response)

if search_response.get("title_results"):
    movie_id = search_response["title_results"][0]["id"]
    print(f"\n🎬 Movie ID Found: {movie_id}")

    # Fetch streaming availability
    sources_url = f"https://api.watchmode.com/v1/title/{movie_id}/sources/"
    sources_params = {"apiKey": WATCHMODE_API_KEY}
    sources_response = requests.get(sources_url, params=sources_params).json()

    print("\n📺 Streaming Sources:")
    for src in sources_response:
        print(f"- {src['name']} ({src['type']}): {src.get('web_url')}")
else:
    print("❌ No title results found.")
