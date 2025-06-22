# 🏡 HomeGPT 2.0

> Your Personal AI Companion – Mood-aware, Memory-driven, Multi-Agent & Multi-Modal.

[![Live App](https://img.shields.io/badge/🚀_Try_Live_App-Streamlit-success?style=for-the-badge)](https://homegpt-20-4eet6dswrhuux7xgvhucwa.streamlit.app/)
[![Built with Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-blueviolet?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![License](https://img.shields.io/github/license/AGBhartariya/HomeGPT-2.0?style=for-the-badge)](LICENSE)

---

## 🌟 Overview

**HomeGPT 2.0** is a beautiful, AI-powered productivity and emotional companion app that offers:
- Mood detection (Gemini AI)
- Telegram message handling
- YouTube music playback
- Movie recommendations
- Gemini-powered chat
- Memory vault
- Fun quizzes & games
- ...and more!

🌐 [**Live App Link → Click Here**](https://homegpt-20-4eet6dswrhuux7xgvhucwa.streamlit.app/)

---

## 🧠 Features

| 🔹 Tab                 | 💬 Description                                                                                  |
|------------------------|-----------------------------------------------------------------------------------------------|
| **🧘 MoodSpace**       | Detects your current mood using Gemini AI, recommends a **song**, **movie**, and provides a therapy-style message. |
| **🎵 Music Player**    | Searches and plays music via **YouTube** API based on your input.                             |
| **🍿 Movie Finder**    | Finds streaming platforms for any movie using the **Watchmode** API.                          |
| **💌 Message Abhigyan**| Real-time message sending with **Telegram bot integration**. Replies appear in the app.        |
| **📚 Memory Vault**    | Save and reflect on personal memories with timestamps.                                         |
| **🤖 Chat with Gemini**| Use Google Gemini 2.0 Flash for powerful LLM chat.                                             |
| **🎮 Quizzes & Games** | Fun quizzes, word games, and more.                                                            |                                      |

---

## ⚙️ Installation Guide

### ✅ 1. Clone Repository
```bash
git clone https://github.com/AGBhartariya/HomeGPT-2.0.git
cd HomeGPT-2.0
```

### ✅ 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate          # On Linux/Mac
venv\Scripts\activate             # On Windows
```


### ✅ 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### ✅ 4. Configure Streamlit Secrets

Create a file `.streamlit/secrets.toml` in your project root:

```bash
[apis]
gemini_key = "YOUR_GEMINI_API_KEY"
youtube_key = "YOUR_YOUTUBE_API_KEY"
watchmode_key = "YOUR_WATCHMODE_API_KEY"

[bot]
bot_token = "YOUR_TELEGRAM_BOT_TOKEN"
chat_id = "YOUR_TELEGRAM_CHAT_ID"
```


---

## 🚀 Deployment (Streamlit Cloud)

1. Push your code to a new GitHub repository (e.g., HomeGPT-2.0)
2. Visit [Streamlit Cloud](https://share.streamlit.io) and sign in
3. Click "New App" → Select your GitHub repo
4. Configure secrets from the Streamlit dashboard (Settings → Secrets)
5. Click Deploy

💡 **After any update:**  
Use “Reboot App” from Streamlit Cloud to clear cache and apply changes.

---
---

## 👨‍💻 Developer

**Abhigyan Gopal Bhartariya**  
[LinkedIn](#https://www.linkedin.com/in/abhigyan-bhartariya-73267928a/)

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙌 Support This Project

If you love HomeGPT-2.0, consider:

- ⭐ Starring this repository
- 🗣 Sharing it with friends and on social media
- 👀 Forking to create your own version
- 🧠 Submitting ideas or pull requests

---

**How to use:**

1. Copy all the above into a file named `README.md` in your repo root.
2. Run:
```bash
git add README.md
git commit -m "Added new README for HomeGPT-2.0"
git push origin main
```

---

This file is ready for GitHub and public sharing—just copy, paste, and commit!



