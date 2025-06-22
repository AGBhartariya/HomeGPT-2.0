import requests
import streamlit as st
def fetch_replies(bot_token, last_update_id):
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    params = {"timeout": 100}
    if last_update_id is not None:
        params["offset"] = last_update_id + 1

    try:
        response = requests.get(url, params=params)
        result = response.json()
        if "result" in result and isinstance(result["result"], list):
            return result["result"]  # Ensure it's a list
        else:
            return []
    except Exception as e:
        print("Error fetching replies:", e)
        return []

