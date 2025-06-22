


import streamlit as st
import sqlite3
import hashlib
import time
import requests
from streamlit_lottie import st_lottie
import json
import os
from datetime import datetime
import pandas as pd
import random
import base64

# Import your existing modules
from utils.gpt_chat import *
from utils.games import *
from utils.quiz_utils import *
from utils.send_love import *
from utils.surprise import *
from utils.face_recog_temp import save_password, retrieve_password, capture_live_image


# Ensure required folders exist
os.makedirs("sync_folder", exist_ok=True)
os.makedirs("assets/photos", exist_ok=True)
os.makedirs("faces", exist_ok=True)

st.set_page_config(
        page_title="HomeGPT - Welcome Home!",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="collapsed"  # Hide sidebar initially
    )



def search_youtube(query, api_key):
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query + " song",
        "key": api_key,
        "type": "video",
        "maxResults": 1,
        "videoCategoryId": "10"  # Music
    }
    response = requests.get(search_url, params=params)
    results = response.json()
    if results.get("items"):
        video_id = results["items"][0]["id"]["videoId"]
        title = results["items"][0]["snippet"]["title"]
        return video_id, title
    return None, None


def autoplay_audio(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    md = f"""
        <audio autoplay="true">
        <source src="data:audio/wav;base64,{b64}" type="audio/wav">
        </audio>
        """
    st.markdown(md, unsafe_allow_html=True)




def load_lottie_url(url: str):
    """Load Lottie animation from URL"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def load_lottie_file(filepath: str):
    """Load Lottie animation from local file"""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except:
        return None

# def play_sound(sound_file):
#     """Play sound file"""
#     try:
#         if os.path.exists(f"assets/{sound_file}"):
#             pygame.mixer.music.load(f"assets/{sound_file}")
#             pygame.mixer.music.play()
#     except:
#         pass

def play_sound(sound_file):
    if os.path.exists(f"assets/{sound_file}"):
        with open(f"assets/{sound_file}", "rb") as f:
            audio_bytes = f.read()
            st.audio(audio_bytes, format="audio/wav")


def play_sound_base64(sound_file):
    """Play sound using base64 encoding for Streamlit"""
    try:
        with open(sound_file, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
            <audio autoplay>
            <source src="data:audio/wav;base64,{b64}" type="audio/wav">
            </audio>
            """
            st.markdown(md, unsafe_allow_html=True)
    except:
        pass

# def init_database():
#     """Initialize the user database"""
#     conn = sqlite3.connect('passwords.db')
#     c = conn.cursor()
    
#     c.execute('''CREATE TABLE IF NOT EXISTS users
#                  (username TEXT PRIMARY KEY, 
#                   password TEXT, 
#                   full_name TEXT,
#                   login_count INTEGER DEFAULT 0,
#                   last_login TEXT,
#                   favorite_color TEXT,
#                   profile_emoji TEXT)''')
    
#     # Add default users (your parents) if they don't exist
#     default_users = [
#         ('Maa', 'mom123', 'Dear Maa', '#FF69B4', '👩‍❤️‍👨'),
#         ('Papa', 'dad123', 'Dear Papa', '#4169E1', '👨‍👩‍👧‍👦'),
#         ('Guest', 'guest123', '', '#32CD32', '👤')
#     ]
    
#     for username, password, full_name, color, emoji in default_users:
#         hashed_password = hashlib.sha256(password.encode()).hexdigest()
#         try:
#             c.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, 0, '', ?, ?)", 
#                      (username, hashed_password, full_name, color, emoji))
#         except:
#             pass
    
#     conn.commit()
#     conn.close()

# def verify_user(username, password):
#     """Verify user credentials"""
#     conn = sqlite3.connect('passwords.db')
#     c = conn.cursor()
    
#     hashed_password = hashlib.sha256(password.encode()).hexdigest()
#     c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
#     user = c.fetchone()
    
#     if user:
#         # Update login count and last login
#         c.execute("UPDATE users SET login_count=login_count+1, last_login=? WHERE username=?", 
#                  (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), username))
#         conn.commit()
    
#     conn.close()
#     return user

# def get_user_info(username):
#     """Get user information"""
#     conn = sqlite3.connect('passwords.db')
#     c = conn.cursor()
#     c.execute("SELECT * FROM users WHERE username=?", (username,))
#     user = c.fetchone()
#     conn.close()
#     return user

# def create_login_page():
#     """Create the main login page"""
    

#     st.markdown("""
#         <style>
#         /* Change selectbox main text and dropdown options to purple */
#         div[data-baseweb="select"] > div {
#             color: #800080 !important;              /* Main selected text */
#             background-color: #f3e6fa !important;   /* Light purple background */
#             font-weight: bold !important;
#         }
#         ul[role="listbox"] > li {
#             color: #800080 !important;              /* Dropdown options text */
#             background-color: #f3e6fa !important;   /* Dropdown options background */
#             font-weight: bold !important;
#         }
#         </style>
#     """, unsafe_allow_html=True)


#     st.markdown("""
#     <style>
#     .main-header {
#         font-size: 3rem !important;
#         color: #2E86AB;
#         text-align: center;
#         font-family: 'Comic Sans MS', cursive;
#         margin-bottom: 2rem;
#         text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
#     }
    
#     .welcome-message {
#         font-size: 1.5rem;
#         color: #5D737E;
#         text-align: center;
#         margin-bottom: 2rem;
#         font-family: 'Arial', sans-serif;
#     }
    
#     .login-container {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 2rem;
#         border-radius: 20px;
#         box-shadow: 0 10px 30px rgba(0,0,0,0.2);
#         margin: 2rem 0;
#     }
    
#     .stButton > button {
#         background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
#         color: white;
#         font-size: 1.2rem !important;
#         font-weight: bold;
#         border: none;
#         border-radius: 50px;
#         padding: 0.75rem 2rem;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.2);
#     }
    
#     .stButton > button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 20px rgba(0,0,0,0.3);
#     }
    
    
    
#     .stSelectbox > div > div {
#         font-size: 1.1rem;
#         background-color: white;
#         border-radius: 10px;
#     }
    
#     .stTextInput > div > div > input {
#         font-size: 1.1rem;
#         padding: 0.75rem;
#         border-radius: 10px;
#         border: 2px solid #ddd;
#     }
    
#     .fun-fact {
#     background: #e3f0fb !important;
#     padding: 1rem !important;
#     border-radius: 10px !important;
#     border-left: 5px solid #2196F3 !important;
#     margin: 1rem 0 !important;
#     color: #1565c0 !important;
#     font-size: 1.1rem !important;
#     }

    
#     .time-greeting {
#         font-size: 1.2rem;
#         color: #6C757D;
#         text-align: center;
#         margin-bottom: 1rem;
#     }
#     </style>
#     """, unsafe_allow_html=True)
    
#     # Initialize session state
#     if 'authenticated' not in st.session_state:
#         st.session_state.authenticated = False
#     if 'user_info' not in st.session_state:
#         st.session_state.user_info = None
#     if 'show_password' not in st.session_state:
#         st.session_state.show_password = False
    
#     # Main header with animation
#     col1, col2, col3 = st.columns([1, 2, 1])
    
#     import pytz
#     # Get current UTC time
#     utc_now = datetime.now(pytz.utc)

#     # Convert to IST
#     ist = pytz.timezone('Asia/Kolkata')
#     ist_now = utc_now.astimezone(ist)
#     current_hour_ist = ist_now.hour

#     with col2:
#         # Load and display Lottie animation
#         lottie_home = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_puciaact.json")
#         if lottie_home:
#             st_lottie(lottie_home, height=200, key="home_animation")
        
#         st.markdown('<h1 class="main-header">🏠 Welcome to HomeGPT! 🏠</h1>', unsafe_allow_html=True)
        
#         # Time-based greeting
        
#         if 5 <= current_hour_ist < 12:
#             greeting = "Good Morning! ☀️"
#         elif 12 <= current_hour_ist < 17:
#             greeting = "Good Afternoon! 🌤️"
#         elif 17 <= current_hour_ist < 21:
#             greeting = "Good Evening! 🌅"
#         else:
#             greeting = "Good Night! 🌙"
        
#         st.markdown(f'<div class="time-greeting">{greeting}</div>', unsafe_allow_html=True)
#         st.markdown('<div class="welcome-message">Your personal AI assistant is ready to help! 💖</div>', unsafe_allow_html=True)
    
#     # Login form
#     with st.container():
#         st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
#         col1, col2, col3 = st.columns([1, 2, 1])
        
#         with col2:
#             st.markdown("### 🔐 Please Sign In")
            
#             # User selection with emojis
#             user_options = {
#                 "👩‍❤️‍👨 Maa": "Maa",
#                 "👨‍👩‍👧‍👦 Papa": "Papa", 
#                 "👤 Guest": "Guest"
#             }
            
#             selected_user = st.selectbox(
#                 "Who's logging in today?",
#                 options=list(user_options.keys()),
#                 index=0,
#                 help="Select your name to continue"
#             )
            
#             username = user_options[selected_user]
            
#             # Password input with show/hide option
#             col_pass1, col_pass2 = st.columns([3, 1])
            
#             with col_pass1:
#                 if st.session_state.show_password:
#                     password = st.text_input("Password", type="default", help="Enter your password")
#                 else:
#                     password = st.text_input("Password", type="password", help="Enter your password")
            
#             with col_pass2:
#                 if st.button("👁️"):
#                     st.session_state.show_password = not st.session_state.show_password
#                     st.rerun()
            
#             # Caps lock warning
#             if password and password.isupper() and len(password) > 2:
#                 st.warning("⚠️ Caps Lock might be ON!")
            
#             # Login button
#             if st.button("🚀 Let's Go!", key="login_btn", use_container_width=True):
#                 if username and password:
#                     user = verify_user(username, password)
#                     if user:
#                         st.session_state.authenticated = True
#                         st.session_state.user_info = user
#                         st.session_state.user_name = user[2]  # Set user_name for compatibility
#                         autoplay_audio("assets/Welcome.wav")

                        
#                         # Success animation
#                         success_lottie = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_s2lryxtd.json")
#                         if success_lottie:
#                             st_lottie(success_lottie, height=150, key="success_animation")
                        
#                         st.success(f"🎉 Welcome back, {user[2]}! Great to see you!")
#                         st.balloons()
#                         time.sleep(2)
#                         st.rerun()
#                     else:
#                         autoplay_audio("assets/Forget.wav")
#                         st.error("🔒 Oops! That password doesn't match. Please try again!")
                        
#                         # Error animation
#                         error_lottie = load_lottie_url("https://assets7.lottiefiles.com/packages/lf20_ddxv3rxw.json")
#                         if error_lottie:
#                             st_lottie(error_lottie, height=100, key="error_animation")
#                 else:
#                     st.warning("Please fill in all fields!")
            
#             # Fun fact section
#             st.markdown("---")
#             st.markdown("""
#             <div class="fun-fact">
#                 <strong>💡 Fun Fact:</strong> This HomeGPT was made with lots of love just for you! 
#                 It has games, quizzes, chat features, and many more surprises! 🎁
#             </div>
#             """, unsafe_allow_html=True)
        
#         st.markdown('</div>', unsafe_allow_html=True)

# MEMORY_FILE = "memories.json"

# def save_memory(title, content, user):
#     memory = {
#         "title": title,
#         "content": content,
#         "user": user,
#         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     }
#     # Load existing memories
#     if os.path.exists(MEMORY_FILE):
#         with open(MEMORY_FILE, "r") as f:
#             try:
#                 memories = json.load(f)
#             except json.JSONDecodeError:
#                 memories = []
#     else:
#         memories = []
#     # Add new memory
#     memories.append(memory)
#     with open(MEMORY_FILE, "w") as f:
#         json.dump(memories, f, indent=2)

# def load_memories(user):
#     if not os.path.exists(MEMORY_FILE):
#         return []
#     with open(MEMORY_FILE, "r") as f:
#         try:
#             memories = json.load(f)
#         except json.JSONDecodeError:
#             memories = []
#     # Filter for current user
#     return [m for m in memories if m["user"] == user]

import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

lottie_balloons = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_3zr20t7m.json")


import sqlite3
import pytz

def show_welcome_animation():
    st.markdown("""
        <style>
            .main-header {
                font-size: 36px;
                font-weight: bold;
                text-align: center;
                color: #4CAF50;
                margin-bottom: 0.5em;
            }
            .time-greeting {
                font-size: 28px;
                text-align: center;
                color: #FF9800;
                margin-top: 0.3em;
            }
            .welcome-message {
                font-size: 20px;
                text-align: center;
                color: #2196F3;
                margin-top: 0.5em;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Get current IST time
        ist = pytz.timezone('Asia/Kolkata')
        ist_now = datetime.now(pytz.utc).astimezone(ist)
        current_hour_ist = ist_now.hour

        # Lottie animation
        lottie_home = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_puciaact.json")
        if lottie_home:
            st_lottie(lottie_home, height=200, key="home_animation")

        # Header and time-based greeting
        st.markdown('<h1 class="main-header">🏠 Welcome to HomeGPT! 🏠</h1>', unsafe_allow_html=True)
        if 5 <= current_hour_ist < 12:
            greeting = "Good Morning! ☀️"
        elif 12 <= current_hour_ist < 17:
            greeting = "Good Afternoon! 🌤️"
        elif 17 <= current_hour_ist < 21:
            greeting = "Good Evening! 🌅"
        else:
            greeting = "Good Night! 🌙"
        st.markdown(f'<div class="time-greeting">{greeting}</div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-message">Your personal AI assistant is ready to help! 💖</div>', unsafe_allow_html=True)


def login_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user


from datetime import datetime

def update_login_details(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        UPDATE users
        SET login_count = login_count + 1,
            last_login = ?
        WHERE username = ?
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), username))
    conn.commit()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    updated_user = c.fetchone()
    conn.close()
    return updated_user

def init_database():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            login_count INTEGER DEFAULT 0,
            last_login TEXT
        )
    """)
    try:
        c.execute("ALTER TABLE users ADD COLUMN login_count INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    try:
        c.execute("ALTER TABLE users ADD COLUMN last_login TEXT")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()


def register_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO users (username, password, login_count, last_login)
            VALUES (?, ?, 0, NULL)
        """, (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()



def create_login_page():

    show_welcome_animation()
    

    tab1, tab2 = st.tabs(["🔓 Login", "🆕 Register"])

    with tab1:
        st.subheader("🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # if st.button("🚀 Login"):
        #     user = login_user(username, password)
        #     if user:
        #         updated_user = update_login_details(username)
        #         st.session_state.authenticated = True
        #         st.session_state.user_info = updated_user
        #         st.success(f"Welcome back, {username}!")
        #         st.markdown(
        #             """<audio autoplay><source src="https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg" type="audio/ogg"></audio>""",
        #             unsafe_allow_html=True,
        #         )
        #         # autoplay_audio("assets/Welcome.wav")
        #         if lottie_balloons:
        #             st_lottie(lottie_balloons, height=250, loop=False)
        #         st.balloons()
        #         st.rerun()
        if st.button("🚀 Login"):
            username = st.session_state.get("login_username", username)
            password = st.session_state.get("login_password", password)
            user = login_user(username, password)
            if user:
                updated_user = update_login_details(username)
                st.session_state.authenticated = True
                st.session_state.user_info = updated_user

                # Show welcome message and animations **before** rerun
                st.success(f"Welcome back, {username}!")

                # 🎵 Play welcome sound using HTML5 <audio>
                st.markdown(
                    """<audio autoplay>
                        <source src="https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg" type="audio/ogg">
                    </audio>""",
                    unsafe_allow_html=True,
                )

                # 🎈 Play balloon animation
                if lottie_balloons:
                    st_lottie(lottie_balloons, height=250, loop=False)

                # 🎉 Show confetti balloons
                st.balloons()

                # Give animations time to finish before rerunning
                time.sleep(2.5)

                # Rerun after delay
                st.rerun()
            else:
                st.error("Invalid username or password")
                st.markdown(
                    """<audio autoplay>
                        <source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg">
                    </audio>""",
                    unsafe_allow_html=True,
                )
        # autoplay_audio("assets/Forget.wav")

            # else:
            #     st.error("Invalid username or password")
            #     st.markdown(
            #         """<audio autoplay><source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg"></audio>""",
            #         unsafe_allow_html=True,
            #     )
            #     autoplay_audio("assets/Forget.wav")

    with tab2:
        st.subheader("🆕 Register")
        username = st.text_input("Choose a Username", key="register_username")
        password = st.text_input("Choose a Password", type="password", key="register_password")
        if st.button("🎉 Register"):
            if username and password:
                success = register_user(username, password)
                if success:
                    st.success("Registration successful! You can now login.")
                    st.balloons()
                else:
                    st.error("Username already exists.")
            else:
                st.warning("Please fill out all required fields.")


if "memories" not in st.session_state:
    st.session_state["memories"] = {}


def create_main_app():
    """Create the main application after login"""
    
    user_info = st.session_state.user_info

    if not user_info:
        st.warning("⚠️ You are not logged in. Please log in to continue.")
        st.session_state['authenticated'] = False
        st.rerun()
        return  # Exit the function early

    username = user_info[0]
    login_count = user_info[2]
    last_login = user_info[3]
    # Page config for main app
    # st.set_page_config(
    #     page_title="HomeGPT: AI Companion for Family",
    #     layout="wide",
    #     page_icon="🏠"
    # )
    
    # Sidebar with user info and logout
    with st.sidebar:
        st.markdown(f"Welcome, {username}!")
        st.markdown(f"**Login Count:** {login_count}")
        if last_login:
            st.markdown(f"**Last Visit:** {last_login}")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_info = None
            st.session_state.user_name = None
            st.rerun()
    
    # Main app content
    st.title(f"🏠 HomeGPT: AI Family Companion")
    st.caption(f"Welcome {username}! 💖")
    



    
    # Initialize quiz session state variables
    if "quiz_mode" not in st.session_state:
        st.session_state.quiz_mode = "Mixed"
    if "question_index" not in st.session_state:
        st.session_state.question_index = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "leaderboard" not in st.session_state:
        st.session_state.leaderboard = []
    if "questions_pool" not in st.session_state:
        st.session_state.questions_pool = []
    if "current_options" not in st.session_state:
        st.session_state.current_options = []
    if "correct_answer" not in st.session_state:
        st.session_state.correct_answer = ""
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = None
    if "show_result" not in st.session_state:
        st.session_state.show_result = False
    
    # Navigation tabs - All tabs from second code integrated
    memory_tab, password_tab, chat_tab, music_tab, games_tab, mood_tab, love_tab = st.tabs([
        "📝 Memory Vault", 
        "🔐 Password Vault",
        "🧠 ChatGPT",
        "🎵 Music",
        "🎮 Games & Quiz",
        "🌤️ MoodSpace",
        "💌 Message"
    ])
    
    from pathlib import Path
    DB_PATH = Path("memories.db")

    def init_memory_db():
        conn = sqlite3.connect("memories.db")
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                username TEXT,
                title TEXT,
                content TEXT,
                timestamp TEXT
            )
        """)
        conn.commit()
        conn.close()

    


    def save_memory(title, content, username):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect("memories.db")
        c = conn.cursor()
        c.execute("INSERT INTO memories (username, title, content, timestamp) VALUES (?, ?, ?, ?)",
                (username, title, content, timestamp))
        conn.commit()
        conn.close()



    def load_memories(username):
        conn = sqlite3.connect("memories.db")
        c = conn.cursor()
        c.execute("SELECT title, content, timestamp FROM memories WHERE username=?", (username,))
        rows = c.fetchall()
        conn.close()
        return [{"title": row[0], "content": row[1], "timestamp": row[2]} for row in rows]



    # You can later replace this with actual database or file-saving logic



    with memory_tab:
        st.header("📝 Record or View Memories")
        title = st.text_input("Memory Title")
        content = st.text_area("Your memory or story")
        if st.button("Save Memory"):
            if title and content:
                save_memory(title, content, username)
                st.success("Memory saved!")
            else:
                st.warning("Please fill in both title and content.")
        init_memory_db()

        st.markdown("---")
        st.subheader("📚 Your Saved Memories")
        memories = load_memories(username)
        if memories:
            for mem in reversed(memories):
                st.markdown(f"**{mem['timestamp']}**  \n*{mem['title']}*  \n{mem['content']}")
                st.markdown("---")
        else:
            st.info("No memories saved yet.")

    
    with password_tab:
        st.header("🔐 Encrypted Password Manager")
        st.info("AES protected password access")
        
        # Password management functionality
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💾 Save Password")
            site_name = st.text_input("Website/App Name")
            password_to_save = st.text_input("Password", type="password")
            if st.button("Save Password"):
                if site_name and password_to_save:
                    success = save_password(site_name, password_to_save, username)
                    if success:
                        st.success("Password saved securely!")
                    else:
                        st.error("Failed to save password")
        
        with col2:
            st.subheader("🔓 Retrieve Password")
            site_to_retrieve = st.text_input("Website/App to retrieve")
            if st.button("Retrieve Password"):
                if site_to_retrieve:
                    password = retrieve_password(site_to_retrieve, username)
                    if password:
                        st.success(f"Password: {password}")
                    else:
                        st.error("Password not found or face verification failed")
    

    
    with chat_tab:
        st.header("🧠 Ask Anything")
        user_query = st.text_input("Talk to HomeGPT:")
        if st.button("Ask"):
            response = ask_homegpt(user_query)
            st.success(response)
    
    with music_tab:
        st.header("🎵 YouTube Music Player")
        song_query = st.text_input("Enter song name or artist:", key="music_search")
        api_key = st.secrets["YOUTUBE_API_KEY"]

        if st.button("Search & Play", key="music_play_btn") and song_query:
            video_id, title = search_youtube(song_query, api_key)
            if video_id:
                st.success(f"Playing: {title}")
                st.video(f"https://www.youtube.com/watch?v={video_id}")
            else:
                st.error("No results found.")

    

    import random
    import time
    import base64
    import pandas as pd
    with games_tab:
        def play_sound(sound_file):
            with open(sound_file, "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                md = f"""
                <audio autoplay>
                <source src="data:audio/wav;base64,{b64}" type="audio/wav">
                </audio>
                """
                st.markdown(md, unsafe_allow_html=True)


        st.header("🎮 Bollywood & Cricket Quiz Game")

        @st.cache_data
        def load_questions():
            df = pd.read_csv("real_bollywood_cricket_quiz_1.csv")
            return df

        df = load_questions()

        if "quiz_mode" not in st.session_state:
            st.session_state.quiz_mode = "Mixed"
        if "question_index" not in st.session_state:
            st.session_state.question_index = 0
        if "score" not in st.session_state:
            st.session_state.score = 0
        if "player_name" not in st.session_state:
            st.session_state.player_name = ""
        if "leaderboard" not in st.session_state:
            st.session_state.leaderboard = []
        if "questions_pool" not in st.session_state:
            st.session_state.questions_pool = []
        if "current_options" not in st.session_state:
            st.session_state.current_options = []
        if "correct_answer" not in st.session_state:
            st.session_state.correct_answer = ""
        if "selected_option" not in st.session_state:
            st.session_state.selected_option = None
        if "show_result" not in st.session_state:
            st.session_state.show_result = False

        def reset_quiz(mode):
            st.session_state.quiz_mode = mode
            if mode == "Bollywood":
                filtered = df[df["category"] == "Bollywood"]
            elif mode == "Cricket":
                filtered = df[df["category"] == "Cricket"]
            else:
                filtered = df

            st.session_state.questions_pool = filtered.sample(frac=1).to_dict("records")
            st.session_state.question_index = 0
            st.session_state.score = 0
            st.session_state.current_options = []
            st.session_state.correct_answer = ""
            st.session_state.selected_option = None
            st.session_state.show_result = False

        if not st.session_state.player_name:
            st.session_state.player_name = st.text_input("👤 Enter your name to begin:")

        st.subheader("🎲 Select Quiz Mode:")
        col1, col2, col3 = st.columns(3)
        if col1.button("🎬 Bollywood"):
            reset_quiz("Bollywood")
            st.rerun()
        if col2.button("🏏 Cricket"):
            reset_quiz("Cricket")
            st.rerun()
        if col3.button("🔀 Mixed"):
            reset_quiz("Mixed")
            st.rerun()

        if st.session_state.questions_pool:
            qlist = st.session_state.questions_pool
            qidx = st.session_state.question_index

            if qidx < min(5,len(qlist)):
                q = qlist[qidx]

                # Shuffle options once
                if not st.session_state.current_options:
                    options = [q["option1"], q["option2"], q["option3"], q["option4"]]
                    random.shuffle(options)
                    st.session_state.current_options = options
                    st.session_state.correct_answer = q["answer"]
                    st.session_state.selected_option = None
                    st.session_state.show_result = False

                options = st.session_state.current_options
                correct = st.session_state.correct_answer

                st.write(f"**Q{qidx+1}:** {q['question']}")
                st.session_state.selected_option = st.radio(
                    "Choose your answer:",
                    options,
                    index=None,
                    key=f"radio_{qidx}"
                )

                if st.button("✅ Submit Answer") and st.session_state.selected_option:
                    if st.session_state.selected_option == correct:
                        st.success("🎉 Correct!")
                        st.session_state.score += 1
                        autoplay_audio("assets/correct.wav")

                    else:
                        st.error(f"❌ Wrong! Correct answer: **{correct}**")
                        autoplay_audio("assets/wrong.wav")

                    st.session_state.show_result = True
                    time.sleep(3)

                    # Move to next question
                    st.session_state.question_index += 1
                    st.session_state.current_options = []
                    st.session_state.selected_option = None
                    st.session_state.correct_answer = ""
                    st.session_state.show_result = False
                    st.rerun()
                # elif st.button("✅ Submit Answer", key=f"submit_{st.session_state.question_index}"):
                #     st.warning("Please select an option before submitting.")

            else:
                st.balloons()
                st.success(f"🏁 Quiz finished, {st.session_state.player_name}!")
                st.success(f"Your Score: {st.session_state.score} / {5}")
                st.session_state.leaderboard.append((st.session_state.player_name, st.session_state.score))
                st.session_state.questions_pool = []

        if st.session_state.leaderboard:
            st.markdown("### 🏆 Leaderboard")
            leaderboard_df = pd.DataFrame(
                st.session_state.leaderboard, columns=["Name", "Score"]
            )
            st.table(leaderboard_df.sort_values("Score", ascending=False).reset_index(drop=True))

        word_scramble_game()
        math_challenge_game()


    
    from utils.gemini_chat import detect_mood_and_recommend, get_youtube_music_video, get_movie_streaming_info

    with mood_tab:
        st.title("🧠 MoodSpace – Your Emotional Companion")
        st.markdown("Tell me how you're feeling today, and I’ll respond with music, movie picks, and a kind word. 🎶🎬💬")

        user_input = st.text_area("💬 How are you feeling today?", placeholder="Write freely about your day or emotions...")

        if st.button("🧭 Analyze My Mood"):
            if not user_input.strip():
                st.warning("Please write something to analyze.")
            else:
                with st.spinner("Analyzing your mood and crafting your personalized experience..."):
                    result = detect_mood_and_recommend(user_input)

                    mood = result["mood"]
                    music = result["music"]
                    movie = result["movie"]
                    therapy = result["therapy"]

                    st.success(f"🎯 Detected Mood: **{mood}**")

                    # 🎵 Music Recommendation
                    st.markdown("### 🎵 Music Recommendation")
                    title, link, thumbnail = get_youtube_music_video(music)
                    if link:
                        st.markdown(f"**{title}**")
                        st.image(thumbnail, width=300)
                        st.markdown(f"[▶️ Watch on YouTube]({link})", unsafe_allow_html=True)
                    else:
                        st.info("No music recommendation found.")

                    # 🎬 Movie Streaming Platforms
                    st.markdown("### 🎬 Movie Recommendation")
                    st.markdown(f"**Suggested Movie/Series**: {movie}")
                    platforms = get_movie_streaming_info(movie)
                    if platforms:
                        st.markdown("**Available on:**")
                        for name, url in platforms:
                            st.markdown(f"📺 [{name}]({url})", unsafe_allow_html=True)
                    else:
                        st.info("No platform availability info found for this title.")

                    # 🧘 Therapy Message
                    st.markdown("### 💬 Therapy Message")
                    st.info(therapy)


                

    from datetime import datetime
    from io import StringIO
    import json
    from utils.send_love import fetch_replies  # Ensure this returns a list of updates

    # Load from Streamlit secrets
    TELEGRAM_BOT_TOKEN = st.secrets["bot"]["bot_token"]
    TELEGRAM_CHAT_ID = st.secrets["bot"]["chat_id"]

    with love_tab:
        st.header("💌 Send a Message to Abhigyan via Telegram")

        # Persistent sender name
        if "sender_name" not in st.session_state:
            st.session_state.sender_name = ""

        name = st.text_input("Your Name", value=st.session_state.sender_name, key="sender_input")
        if name.strip():
            st.session_state.sender_name = name.strip()

        # Session state defaults
        for key, default in {
            "love_messages": [],
            "incoming_replies": {},
            "last_update_id": None,
            "processed_reply_ids": set(),
            "chat_history": [],
            "typing_indicator": False
        }.items():
            if key not in st.session_state:
                st.session_state[key] = default

        # --- Chat input ---
        user_message = st.chat_input("Type your message and press Enter")

        def send_to_telegram(message, sender):
            text = f"📩 Message from {sender}:\n{message}"
            data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
            try:
                response = requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", data=data
                )
                return response.status_code == 200
            except Exception as e:
                print("Telegram send error:", e)
                return False

        # --- Handle sending message ---
        if user_message:
            sender = st.session_state.sender_name.strip()
            if sender:
                sent = send_to_telegram(user_message, sender)
                if sent:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    st.session_state.love_messages.append({
                        "sender": sender,
                        "content": user_message,
                        "timestamp": timestamp
                    })
                    st.session_state.chat_history.append({
                        "role": "user",
                        "name": sender,
                        "text": user_message,
                        "timestamp": timestamp
                    })
                    st.success("✅ Sent to Abhigyan!")
                else:
                    st.error("❌ Failed to send message.")
            else:
                st.warning("Please enter your name before sending a message.")

        # --- Fetch replies from Telegram ---
        updates = fetch_replies(TELEGRAM_BOT_TOKEN, st.session_state.last_update_id)
        for update in updates:
            if isinstance(update, dict):
                update_id = update.get("update_id")
                if update_id in st.session_state.processed_reply_ids:
                    continue

                message = update.get("message", {})
                if message and "text" in message:
                    msg_text = message["text"]
                    st.session_state.last_update_id = update_id
                    st.session_state.processed_reply_ids.add(update_id)

                    if msg_text.startswith("@"):
                        try:
                            user, reply = msg_text.split(" ", 1)
                            user_key = user[1:].strip().lower()

                            if reply not in st.session_state.incoming_replies.get(user_key, []):
                                # 🔔 Show typing indicator
                                st.session_state.typing_indicator = True

                                st.session_state.incoming_replies.setdefault(user_key, []).append(reply)
                                st.session_state.chat_history.append({
                                    "role": "assistant",
                                    "name": "Abhigyan",
                                    "text": reply,
                                    "timestamp": datetime.now().strftime("%H:%M:%S")
                                })
                                # Optional toast notification
                                try:
                                    st.toast(f"💬 New reply from Abhigyan: {reply}")
                                except:
                                    st.info("💬 New reply from Abhigyan received!")
                        except ValueError:
                            continue

        # --- Display chat history (sorted) ---
        chat_history = sorted(
            st.session_state.chat_history,
            key=lambda x: x["timestamp"]
        )

        for entry in chat_history:
            with st.chat_message(entry["role"]):
                st.markdown(f"**{entry['name']}**: {entry['text']}\n\n🕒 _{entry['timestamp']}_")

        # --- Download buttons ---
        with st.expander("📂 Export Chat History"):
            # Download as text
            txt_data = "\n".join(
                f"{msg['role'].capitalize()} {msg['name']} [{msg['timestamp']}]: {msg['text']}"
                for msg in chat_history
            )
            st.download_button("📄 Download as .txt", txt_data, "chat_history.txt")

            # Download as JSON
            json_data = json.dumps(chat_history, indent=2)
            st.download_button("🧾 Download as .json", json_data, "chat_history.json")







                



            




def main():
    """Main application function"""
    
    
    # Initialize session state variables FIRST
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'user_info' not in st.session_state:
        st.session_state['user_info'] = None
    if 'user_name' not in st.session_state:
        st.session_state['user_name'] = None
    if 'loading_complete' not in st.session_state:
        st.session_state['loading_complete'] = False
    
    # Initialize database
    init_database()
    
    # ===== AUTHENTICATION GATE - STOPS EVERYTHING UNTIL LOGIN =====
    if not st.session_state.get('authenticated', False):
        
        # Optional: Show catchy loader on first visit
        if not st.session_state['loading_complete']:
            with st.spinner('✨ Setting up your HomeGPT experience...'):
                time.sleep(2)  # Simulate loading time
            st.session_state['loading_complete'] = True
            st.rerun()
        
        # Show only the authentication page
        create_login_page()
        st.stop()  # ⭐ THIS PREVENTS ANYTHING ELSE FROM LOADING
    
    # ===== ONLY RUNS AFTER SUCCESSFUL AUTHENTICATION =====
    create_main_app()

if __name__ == "__main__":
    main()



