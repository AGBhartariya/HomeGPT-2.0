import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

def ask_homegpt(prompt: str):
    if not prompt or not prompt.strip():
        return "Please ask something 🙂"

    try:
        # Configure API fresh every call (NO caching)
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

        model = genai.GenerativeModel("gemini-2.0-flash")

        response = model.generate_content(
            "You are a very warm, friendly family assistant named HomeGPT. "
            "You provide respectful, caring, and helpful answers.\n\n"
            f"User: {prompt}",
            request_options={"timeout": 15}  # ⛔ stop retry storms
        )

        return response.text

    except ResourceExhausted:
        # 🚫 HARD STOP — prevents retry loops
        return "⚠️ HomeGPT is temporarily unavailable (API quota reached). Please try again later."

    except Exception as e:
        return f"❌ Unexpected error: {e}"

