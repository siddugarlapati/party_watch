import streamlit as st
import uuid
import json
import time
from datetime import datetime
import threading
import asyncio
import os
from dotenv import load_dotenv
from streamlit_webrtc import webrtc_streamer
import requests
from io import BytesIO
from PIL import Image
import pyperclip
import websockets
import html
from pytube import YouTube

# Backend API config
BACKEND_URL = "http://localhost:8000/api"
WS_URL = "ws://localhost:8000/ws"

# Page config
st.set_page_config(
    page_title="PartyWatch - Shared YouTube Rooms",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern UI CSS & JS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&family=Fira+Mono&display=swap');
body, .main, .block-container {
    font-family: 'Montserrat', 'Fira Mono', monospace !important;
    background: linear-gradient(135deg, #0f2027 0%, #2c5364 100%) fixed;
    min-height: 100vh;
}
.main-header {
    font-size: 3.5rem;
    font-weight: 900;
    text-align: center;
    color: #fff;
    letter-spacing: 2px;
    text-shadow: 0 4px 32px #00ffe7, 0 1px 0 #000;
    margin-bottom: 2rem;
    animation: neon-flicker 2s infinite alternate;
}
@keyframes neon-flicker {
    0% { text-shadow: 0 0 8px #00ffe7, 0 1px 0 #000; }
    100% { text-shadow: 0 0 32px #00ffe7, 0 1px 0 #000; }
}
.room-card {
    background: rgba(255,255,255,0.12);
    box-shadow: 0 8px 32px 0 rgba(31,38,135,0.37);
    backdrop-filter: blur(8px);
    border-radius: 18px;
    border: 1.5px solid rgba(255,255,255,0.18);
    margin: 1rem 0;
    padding: 1.5rem;
    color: #fff;
    transition: box-shadow 0.3s;
}
.room-card:hover {
    box-shadow: 0 12px 48px 0 #00ffe7;
}
.stButton > button {
    background: linear-gradient(90deg, #00ffe7 0%, #ff6bcb 100%);
    color: #222;
    font-weight: 700;
    border-radius: 12px;
    border: none;
    padding: 0.7rem 2.2rem;
    font-size: 1.2rem;
    box-shadow: 0 2px 16px #00ffe744;
    transition: transform 0.1s, box-shadow 0.2s;
    cursor: pointer;
}
.stButton > button:hover {
    transform: scale(1.07) rotate(-2deg);
    box-shadow: 0 4px 32px #ff6bcb88;
}
.stTextInput > div > input {
    background: rgba(255,255,255,0.18);
    color: #fff;
    border-radius: 8px;
    border: 1.5px solid #00ffe7;
    font-size: 1.1rem;
    padding: 0.6rem 1rem;
}
.stTextInput > div > input:focus {
    border: 2px solid #ff6bcb;
    outline: none;
}
.chat-message {
    background: linear-gradient(90deg, #00ffe7 0%, #ff6bcb 100%);
    color: #222;
    padding: 0.7rem 1.2rem;
    border-radius: 18px 18px 4px 18px;
    margin: 0.5rem 0;
    font-size: 1.1rem;
    box-shadow: 0 2px 12px #00ffe744;
    animation: chat-pop 0.5s cubic-bezier(.68,-0.55,.27,1.55);
}
@keyframes chat-pop {
    0% { transform: scale(0.7) translateY(30px); opacity: 0; }
    100% { transform: scale(1) translateY(0); opacity: 1; }
}
.user-presence {
    display: inline-block;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: linear-gradient(135deg, #00ffe7 0%, #ff6bcb 100%);
    margin-right: 0.7rem;
    box-shadow: 0 0 8px #00ffe7, 0 0 16px #ff6bcb;
    animation: pulse 1.2s infinite alternate;
}
@keyframes pulse {
    0% { box-shadow: 0 0 8px #00ffe7, 0 0 16px #ff6bcb; }
    100% { box-shadow: 0 0 24px #00ffe7, 0 0 32px #ff6bcb; }
}
.host-badge {
    background: linear-gradient(90deg, #ff6bcb 0%, #00ffe7 100%);
    color: #fff;
    padding: 0.2rem 0.7rem;
    border-radius: 12px;
    font-size: 0.9rem;
    margin-left: 0.7rem;
    font-weight: 700;
    letter-spacing: 1px;
    box-shadow: 0 2px 8px #ff6bcb44;
}
.stForm > form {
    background: rgba(255,255,255,0.10);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    box-shadow: 0 2px 16px #00ffe744;
    margin-bottom: 1.5rem;
}
.stAlert {
    border-radius: 12px !important;
    font-size: 1.1rem;
}
.stMarkdown h2, .stMarkdown h3 {
    color: #00ffe7;
    font-weight: 900;
    letter-spacing: 1px;
}
.stMarkdown ul {
    color: #fff;
}
::-webkit-scrollbar {
    width: 8px;
    background: #222;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #00ffe7 0%, #ff6bcb 100%);
    border-radius: 8px;
}
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
</style>

<!-- Animated background using particles.js -->
<div id="particles-js" style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:-1;"></div>
<script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
<script>
window.addEventListener('DOMContentLoaded', function() {
  if (window.particlesJS) {
    particlesJS('particles-js', {
      "particles": {
        "number": {"value": 60},
        "color": {"value": ["#00ffe7", "#ff6bcb"]},
        "shape": {"type": "circle"},
        "opacity": {"value": 0.5},
        "size": {"value": 6, "random": true},
        "line_linked": {"enable": true, "distance": 120, "color": "#fff", "opacity": 0.2, "width": 1},
        "move": {"enable": true, "speed": 2, "direction": "none", "random": true, "straight": false, "out_mode": "out"}
      },
      "interactivity": {
        "detect_on": "canvas",
        "events": {"onhover": {"enable": true, "mode": "repulse"}, "onclick": {"enable": true, "mode": "push"}},
        "modes": {"repulse": {"distance": 80}, "push": {"particles_nb": 4}}
      },
      "retina_detect": true
    });
  }
});
</script>

<!-- Confetti burst on join/message send -->
<script>
window.confettiBurst = function() {
  const duration = 1 * 1000;
  const animationEnd = Date.now() + duration;
  const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 9999 };
  function randomInRange(min, max) { return Math.random() * (max - min) + min; }
  const interval = setInterval(function() {
    const timeLeft = animationEnd - Date.now();
    if (timeLeft <= 0) { return clearInterval(interval); }
    const particleCount = 30 * (timeLeft / duration);
    confetti(Object.assign({}, defaults, {
      particleCount,
      origin: { x: randomInRange(0.1, 0.9), y: Math.random() - 0.2 }
    }));
  }, 200);
};
</script>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
""", unsafe_allow_html=True)

# Session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if 'room_code' not in st.session_state:
    st.session_state.room_code = None
if 'is_host' not in st.session_state:
    st.session_state.is_host = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'current_video_id' not in st.session_state:
    st.session_state.current_video_id = None
if 'playback_state' not in st.session_state:
    st.session_state.playback_state = {'playing': False, 'current_time': 0}
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'room_users' not in st.session_state:
    st.session_state.room_users = []
if 'room_type' not in st.session_state:
    st.session_state.room_type = 'YouTube'
if 'current_spotify_type' not in st.session_state:
    st.session_state.current_spotify_type = None
if 'current_spotify_id' not in st.session_state:
    st.session_state.current_spotify_id = None
if 'screenshare_role' not in st.session_state:
    st.session_state.screenshare_role = 'Viewer'
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'room_desc' not in st.session_state:
    st.session_state.room_desc = ''
if 'room_password' not in st.session_state:
    st.session_state.room_password = ''
if 'room_is_public' not in st.session_state:
    st.session_state.room_is_public = True
if 'user_status' not in st.session_state:
    st.session_state.user_status = {}
if 'edit_message_id' not in st.session_state:
    st.session_state.edit_message_id = None
if 'edit_message_text' not in st.session_state:
    st.session_state.edit_message_text = ''
if 'pinned_message' not in st.session_state:
    st.session_state.pinned_message = None
if 'unread_count' not in st.session_state:
    st.session_state.unread_count = 0
if 'show_profile' not in st.session_state:
    st.session_state.show_profile = False
if 'media_queue' not in st.session_state:
    st.session_state.media_queue = []
if 'avatar_url' not in st.session_state:
    st.session_state.avatar_url = "https://api.dicebear.com/7.x/avataaars/svg?seed=default"
if 'db' not in st.session_state:
    st.session_state.db = None
if 'private_chats' not in st.session_state:
    st.session_state.private_chats = {}
if 'sprint_board' not in st.session_state:
    st.session_state.sprint_board = {'To Do': [], 'In Progress': [], 'Done': []}
if 'meeting_notes' not in st.session_state:
    st.session_state.meeting_notes = ""
if 'room_info' not in st.session_state:
    st.session_state.room_info = {}

# Security Utility
def sanitize_input(text):
    """Escapes HTML special characters in a string to prevent XSS."""
    if not isinstance(text, str):
        return ""
    return html.escape(text)

# Helper functions
def api_post(path, data):
    try:
        r = requests.post(f"{BACKEND_URL}{path}", json=data)
        r.raise_for_status()
        return r.json()
    except:
        return None

def api_get(path):
    try:
        r = requests.get(f"{BACKEND_URL}{path}")
        r.raise_for_status()
        return r.json()
    except:
        return None

def api_patch(path, data):
    r = requests.patch(f"{BACKEND_URL}{path}", json=data)
    r.raise_for_status()
    return r.json()

def api_delete(path):
    """Make DELETE request to backend API"""
    try:
        response = requests.delete(f"{BACKEND_URL}{path}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API Error: {e}")
        return None

# User online/offline indicators
def set_user_online(user_id):
    st.session_state.user_status[user_id] = 'online'

def set_user_offline(user_id):
    st.session_state.user_status[user_id] = 'offline'

# Invite link sharing
def invite_link(room_code):
    link = f"http://localhost:8501/?room={room_code}"
    if st.button("Copy Invite Link"):
        pyperclip.copy(link)
        st.success("Invite link copied!")
    st.markdown(f"<small>{link}</small>", unsafe_allow_html=True)

# Quick emoji reactions on messages
def message_reactions(msg_id):
    cols = st.columns(5)
    for i, emoji in enumerate(["👍", "😂", "😍", "🔥", "👏"]):
        if cols[i].button(emoji, key=f"react_{msg_id}_{i}"):
            st.toast(f"Reacted {emoji} to message {msg_id}")

def emoji_picker():
    """Simple emoji picker widget"""
    emojis = ["😀", "😂", "😍", "🔥", "👍", "👎", "❤️", "🎉", "🎵", "🎬"]
    cols = st.columns(len(emojis))
    for i, emoji in enumerate(emojis):
        if cols[i].button(emoji, key=f"emoji_{i}"):
            return emoji
    return None

# Improved queue: drag-and-drop (desktop)
def queue_widget():
    st.markdown("**Queue / Playlist**")
    with st.form("queue_form"):
        url = st.text_input("Add YouTube/Spotify URL to queue")
        add = st.form_submit_button("Add to Queue")
        if add and url:
            st.session_state.media_queue.append({"url": url, "votes": 0})
    # Drag-and-drop reordering (desktop only, demo)
    if st.session_state.media_queue:
        st.markdown("**Drag to reorder (desktop):**")
        for i, item in enumerate(st.session_state.media_queue):
            st.write(f"{i+1}. {item['url']}")
            up = st.button("⬆️", key=f"queue_up_{i}")
            down = st.button("⬇️", key=f"queue_down_{i}")
            if up and i > 0:
                st.session_state.media_queue[i-1], st.session_state.media_queue[i] = st.session_state.media_queue[i], st.session_state.media_queue[i-1]
            if down and i < len(st.session_state.media_queue)-1:
                st.session_state.media_queue[i+1], st.session_state.media_queue[i] = st.session_state.media_queue[i], st.session_state.media_queue[i+1]
        st.markdown("**Top voted:**")
        top = max(st.session_state.media_queue, key=lambda x: x["votes"])
        st.write(top["url"])

# User profile page
def user_profile():
    st.markdown(f"<h2>Profile: {st.session_state.username}</h2>", unsafe_allow_html=True)
    st.image(st.session_state.avatar_url, width=96)
    st.write(f"User ID: {st.session_state.user_id}")
    st.write(f"Recent rooms: {st.session_state.room_code}")
    st.write(f"Friends: (demo) None yet")
    if st.button("Back to Room"):
        st.session_state.show_profile = False

# Theme toggle
def theme_css():
    if st.session_state.theme == 'dark':
        return """
        <style>
        body, .main, .block-container {
            background: linear-gradient(135deg, #0f2027 0%, #2c5364 100%) fixed !important;
            color: #fff !important;
        }
        .room-card, .stForm > form {
            background: rgba(30,30,40,0.92) !important;
            color: #fff !important;
        }
        .chat-message { background: linear-gradient(90deg, #00ffe7 0%, #ff6bcb 100%); color: #222; }
        </style>
        """
    else:
        return """
        <style>
        body, .main, .block-container {
            background: linear-gradient(135deg, #f0f2f6 0%, #e0e7ef 100%) fixed !important;
            color: #222 !important;
        }
        .room-card, .stForm > form {
            background: rgba(255,255,255,0.92) !important;
            color: #222 !important;
        }
        .chat-message { background: linear-gradient(90deg, #00ffe7 0%, #ff6bcb 100%); color: #222; }
        </style>
        """

def theme_toggle():
    col1, col2 = st.columns([1, 8])
    with col1:
        if st.button('🌙' if st.session_state.theme == 'dark' else '☀️', key='theme_toggle'):
            st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
    with col2:
        st.markdown(f'<span style="font-size:1.2rem;font-weight:700;">{st.session_state.theme.title()} Mode</span>', unsafe_allow_html=True)
    st.markdown(theme_css(), unsafe_allow_html=True)

# Avatar selector widget
def avatar_selector():
    st.subheader("👤 Choose Avatar")
    AVATAR_CHOICES = [
        "https://api.dicebear.com/7.x/avataaars/svg?seed=default",
        "https://api.dicebear.com/7.x/avataaars/svg?seed=john",
        "https://api.dicebear.com/7.x/avataaars/svg?seed=jane",
        "https://api.dicebear.com/7.x/avataaars/svg?seed=mike",
        "https://api.dicebear.com/7.x/avataaars/svg?seed=sarah"
    ]
    
    if st.button("🎲 Random Avatar"):
        st.session_state.avatar_url = AVATAR_CHOICES[0]
    
    cols = st.columns(len(AVATAR_CHOICES))
    for i, url in enumerate(AVATAR_CHOICES):
        with cols[i]:
            if st.button(f"Avatar {i+1}", key=f"avatar_{i}"):
                st.session_state.avatar_url = url

# WebSocket for real-time chat/presence
async def ws_listen(room_code, on_message):
    async with websockets.connect(f"{WS_URL}/{room_code}") as ws:
        while True:
            msg = await ws.recv()
            on_message(msg)

def create_room(video_url, room_name):
    """Create a new YouTube room"""
    try:
        # Extract video ID from YouTube URL
        yt = YouTube(video_url)
        video_id = yt.video_id
        
        # Generate room code
        room_code = str(uuid.uuid4())[:8].upper()
        
        # Create room data
        room_data = {
            "room_code": room_code,
            "host_id": st.session_state.user_id,
            "video_id": video_id,
            "room_name": room_name,
            "room_type": "YouTube"
        }
        
        # Call API to create room
        result = api_post("/rooms", room_data)
        if result:
            st.session_state.room_code = room_code
            st.session_state.is_host = True
            st.session_state.username = room_name
            st.session_state.room_type = 'YouTube'
            st.session_state.current_video_id = video_id
            st.session_state.room_desc = f"Watching: {yt.title}"
            st.session_state.room_is_public = True
            st.session_state.room_password = None
            return room_code
        return None
    except Exception as e:
        st.error(f"Error creating room: {e}")
        return None

def create_spotify_room(spotify_url, room_name):
    """Create a new Spotify room"""
    try:
        # Extract Spotify ID and type from URL
        if "track/" in spotify_url:
            spotify_type = "track"
            spotify_id = spotify_url.split("track/")[1].split("?")[0]
        elif "playlist/" in spotify_url:
            spotify_type = "playlist"
            spotify_id = spotify_url.split("playlist/")[1].split("?")[0]
        elif "album/" in spotify_url:
            spotify_type = "album"
            spotify_id = spotify_url.split("album/")[1].split("?")[0]
        else:
            st.error("Invalid Spotify URL")
            return None
        
        # Generate room code
        room_code = str(uuid.uuid4())[:8].upper()
        
        # Create room data
        room_data = {
            "room_code": room_code,
            "host_id": st.session_state.user_id,
            "spotify_type": spotify_type,
            "spotify_id": spotify_id,
            "room_name": room_name,
            "room_type": "Spotify"
        }
        
        # Call API to create room
        result = api_post("/rooms", room_data)
        if result:
            st.session_state.room_code = room_code
            st.session_state.is_host = True
            st.session_state.username = room_name
            st.session_state.room_type = 'Spotify'
            st.session_state.current_spotify_type = spotify_type
            st.session_state.current_spotify_id = spotify_id
            st.session_state.room_desc = f"Listening to Spotify {spotify_type}"
            st.session_state.room_is_public = True
            st.session_state.room_password = None
            return room_code
        return None
    except Exception as e:
        st.error(f"Error creating Spotify room: {e}")
        return None

def join_room_ui():
    """Renders a unified UI for joining any room and handles the join logic."""
    st.subheader("Join a Room")
    with st.form("join_room_form"):
        join_code = st.text_input("Room Code", placeholder="Enter 8-character code")
        join_name = st.text_input("Your Name", key="join_name")
        password = st.text_input("Room Password (if required)", type="password", key="join_room_password")
        join_button = st.form_submit_button("Join Room")

        if join_button and join_code and join_name:
            with st.spinner(f"Joining room {join_code.upper()}..."):
                try:
                    # Sanitize username before sending to backend
                    safe_username = sanitize_input(join_name)
                    if not safe_username:
                        st.warning("Please enter a valid name.")
                        return

                    join_data = {
                        "user_id": st.session_state.user_id,
                        "username": safe_username
                    }
                    if password:
                        join_data["password"] = password

                    result = api_post(f"/rooms/{join_code.upper()}/join", join_data)

                    if result:
                        st.session_state.room_code = join_code.upper()
                        st.session_state.is_host = False
                        st.session_state.username = safe_username

                        # Update state from backend response
                        st.session_state.room_info = result
                        st.session_state.room_type = result.get("room_type", "YouTube")
                        st.session_state.current_video_id = result.get("video_id")
                        st.session_state.current_spotify_type = result.get("spotify_type")
                        st.session_state.current_spotify_id = result.get("spotify_id")
                        st.session_state.room_desc = result.get("room_desc", "")
                        st.session_state.room_is_public = result.get("is_public", True)

                        st.success("Successfully joined room!")
                        st.markdown('<script>window.confettiBurst && window.confettiBurst();</script>', unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.error("Invalid room code or password.")
                except requests.HTTPError as e:
                    if e.response.status_code == 403:
                        st.error("Incorrect password or you are not authorized to join.")
                    else:
                        st.error("Invalid room code or the room may not exist.")
                except Exception as e:
                    st.error(f"An error occurred while joining the room: {e}")

def render_youtube_player(video_id, is_host):
    """Render YouTube player with controls"""
    st.subheader("🎬 YouTube Player")
    
    # YouTube embed
    youtube_embed = f"""
    <iframe 
        width="100%" 
        height="400" 
        src="https://www.youtube.com/embed/{video_id}?enablejsapi=1&origin={st.get_option('server.baseUrlPath')}" 
        frameborder="0" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
    """
    st.markdown(youtube_embed, unsafe_allow_html=True)
    
    # Playback controls (host only)
    if is_host:
        st.subheader("🎮 Playback Controls")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("⏮️ Previous"):
                st.info("Previous track functionality")
        
        with col2:
            if st.button("⏯️ Play/Pause"):
                st.info("Play/Pause functionality")
        
        with col3:
            if st.button("⏭️ Next"):
                st.info("Next track functionality")
        
        with col4:
            if st.button("🔊 Volume"):
                st.info("Volume control")
        
        # Progress bar
        progress = st.slider("Progress", 0, 100, 50, key="video_progress")
        st.progress(progress / 100)

def render_spotify_embed(spotify_type, spotify_id):
    """Render Spotify embed player"""
    st.subheader("🎵 Spotify Player")
    
    if spotify_type and spotify_id:
        spotify_embed = f"""
        <iframe 
            style="border-radius:12px" 
            src="https://open.spotify.com/embed/{spotify_type}/{spotify_id}?utm_source=generator" 
            width="100%" 
            height="352" 
            frameborder="0" 
            allowfullscreen="" 
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
            loading="lazy">
        </iframe>
        """
        st.markdown(spotify_embed, unsafe_allow_html=True)
    else:
        st.warning("No Spotify content loaded")

def render_user_presence():
    """Render users in room with presence indicators"""
    st.subheader("👤 Room Members")
    room_info = st.session_state.get('room_info', {})
    if not room_info:
        st.info("Loading room members...")
        return
    
    for user in room_info.get('users', []):
        is_host = user.get('id') == room_info.get('host_id')
        username = sanitize_input(user.get('username', f"User {user.get('id', '')[:8]}"))
        status = st.session_state.user_status.get(user.get('id'), 'online')
        status_dot = '<span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:{};margin-right:0.5rem;"></span>'.format('#4CAF50' if status=='online' else '#aaa')
        profile_btn = ''
        if user.get('id') == st.session_state.user_id:
            profile_btn = '<button onclick="window.location.href=\'#profile\'">Profile</button>'
        st.markdown(f"""
        <div style="margin: 0.5rem 0;">
            {status_dot}
            {username}
            {'<span class="host-badge">HOST</span>' if is_host else ''}
            {profile_btn}
        </div>
        """, unsafe_allow_html=True)

def render_chat_section():
    # Reset unread count as soon as the user sees the chat section
    subheader_text = "💬 Chat"
    if st.session_state.unread_count > 0:
        subheader_text += f" ({st.session_state.unread_count} new)"
    st.subheader(subheader_text)
    st.session_state.unread_count = 0
    
    if st.session_state.pinned_message:
        st.markdown(f"<div style='background:#ffeaa7;padding:0.5rem 1rem;border-radius:8px;margin-bottom:0.5rem;'><b>Pinned:</b> {st.session_state.pinned_message}</div>", unsafe_allow_html=True)
    chat_container = st.container()
    with chat_container:
        for idx, msg in enumerate(st.session_state.chat_messages[-20:]):
            timestamp = datetime.fromisoformat(msg['timestamp']).strftime("%H:%M")
            avatar_html = f'<img src="{st.session_state.avatar_url}" style="width:32px;height:32px;border-radius:50%;vertical-align:middle;margin-right:8px;">' if st.session_state.avatar_url else ''
            
            # Sanitize content before rendering
            username_html = sanitize_input(msg.get('username'))
            raw_message = msg.get('message', '')

            if raw_message.startswith('GIF:'):
                gif_url = sanitize_input(raw_message[4:]) # Sanitize the URL part
                msg_html = f'<img src="{gif_url}" style="max-width:120px;max-height:120px;border-radius:12px;">'
            else:
                msg_html = sanitize_input(raw_message)

            st.markdown(f"""
            <div class="chat-message">
                {avatar_html}<strong>{username_html}</strong> <small>({timestamp})</small><br>
                {msg_html}
            </div>
            """, unsafe_allow_html=True)
            # Quick reactions
            message_reactions(idx)
            # Edit/delete for sender
            if msg['user_id'] == st.session_state.user_id:
                if st.button("Edit", key=f"edit_{idx}"):
                    st.session_state.edit_message_id = idx
                    st.session_state.edit_message_text = msg['message']
                if st.button("Delete", key=f"delete_{idx}"):
                    st.session_state.chat_messages.pop(idx)
                    st.rerun()
            # Pin for host
            if st.session_state.is_host and st.button("Pin", key=f"pin_{idx}"):
                st.session_state.pinned_message = msg['message']
    # Edit message form
    if st.session_state.edit_message_id is not None:
        with st.form("edit_message_form"):
            new_text = st.text_input("Edit your message", value=st.session_state.edit_message_text)
            save = st.form_submit_button("Save")
            cancel = st.form_submit_button("Cancel")
            if save:
                st.session_state.chat_messages[st.session_state.edit_message_id]['message'] = new_text
                st.session_state.edit_message_id = None
                st.session_state.edit_message_text = ''
                st.rerun()
            if cancel:
                st.session_state.edit_message_id = None
                st.session_state.edit_message_text = ''
                st.rerun()
    with st.form("chat_form"):
        col1, col2 = st.columns([4, 1])
        with col1:
            message = st.text_input("Type your message...", key="chat_input")
        with col2:
            emoji = emoji_picker()
            if emoji:
                st.session_state['chat_input'] = (st.session_state.get('chat_input') or '') + emoji
        
        send = st.form_submit_button("Send")
        if send and message:
            # Send message via API
            try:
                chat_data = {
                    "room_code": st.session_state.room_code,
                    "user_id": st.session_state.user_id,
                    "username": st.session_state.username,
                    "message": sanitize_input(message) # Sanitize on the way out
                }
                result = api_post("/chat/messages", chat_data)
                if result:
                    # Instantly add message to local state for responsiveness
                    st.session_state.chat_messages.append(result)
                    st.session_state.unread_count = 0 # Reset own unread count
                    st.rerun()
            except Exception as e:
                st.error(f"Error sending message: {e}")
        
        # Send GIF
        gif_url = st.text_input("Or send a GIF URL", placeholder="https://media.giphy.com/...")
        if st.button("Send GIF") and gif_url:
            try:
                # Sanitize the GIF url before creating the special message format
                safe_gif_url = sanitize_input(gif_url)
                chat_data = {
                    "room_code": st.session_state.room_code,
                    "user_id": st.session_state.user_id,
                    "username": st.session_state.username,
                    "message": f"GIF:{safe_gif_url}" # Sanitize on the way out
                }
                result = api_post("/chat/messages", chat_data)
                if result:
                    # Instantly add message to local state for responsiveness
                    st.session_state.chat_messages.append(result)
                    st.rerun()
            except Exception as e:
                st.error(f"Error sending GIF: {e}")

def poll_widget():
    """Render poll widget"""
    st.subheader("🎲 Quick Poll")
    
    with st.expander("Create a poll"):
        poll_question = st.text_input("Poll Question", key="poll_question")
        poll_options = st.text_area("Options (one per line)", key="poll_options")
        
        if st.button("Create Poll") and poll_question and poll_options:
            options = [opt.strip() for opt in poll_options.split('\n') if opt.strip()]
            if len(options) >= 2:
                st.success("Poll created!")
                st.session_state.current_poll = {
                    "question": poll_question,
                    "options": options,
                    "votes": {opt: 0 for opt in options}
                }
            else:
                st.error("Need at least 2 options")
    
    # Display current poll
    if hasattr(st.session_state, 'current_poll') and st.session_state.current_poll:
        poll = st.session_state.current_poll
        st.write(f"**{poll['question']}**")
        
        for option in poll['options']:
            votes = poll['votes'][option]
            total_votes = sum(poll['votes'].values())
            percentage = (votes / total_votes * 100) if total_votes > 0 else 0
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(percentage / 100)
            with col2:
                if st.button(f"Vote ({votes})", key=f"vote_{option}"):
                    poll['votes'][option] += 1
                    st.rerun()

def work_mode_ui():
    """Work mode UI with professional features"""
    st.markdown("""
    <style>
    body, .main, .block-container {
        font-family: 'Segoe UI', 'Fira Mono', monospace !important;
        background: #f4f6fa !important;
        color: #222 !important;
    }
    .main-header { 
        color: #2d3a4a !important; 
        text-shadow: none !important; 
        font-size: 2.5rem !important;
    }
    .work-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #007acc;
    }
    .sprint-column {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem;
        min-height: 200px;
        border: 2px dashed #dee2e6;
    }
    .task-item {
        background: white;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 6px;
        border-left: 3px solid #007acc;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .meeting-notes {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">💼 PartyWatch Work Mode</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #6c757d;">Run your sprints, meetings, and collaborate professionally</p>', unsafe_allow_html=True)
    
    # Work mode tabs
    work_tab = st.tabs(["📋 Sprint Board", "📝 Meeting Notes", "💬 Chat", "📹 Video Call", "⚙️ Settings"])
    
    with work_tab[0]:  # Sprint Board
        st.markdown('<div class="work-card">', unsafe_allow_html=True)
        st.subheader("🎯 Sprint Board")
        
        # Load sprint board from API
        if st.session_state.room_code:
            try:
                sprint_data = api_get(f"/sprint/{st.session_state.room_code}")
                if sprint_data:
                    st.session_state.sprint_board = sprint_data
            except:
                pass
        
        # Sprint Board UI
        cols = st.columns(3)
        for i, col_name in enumerate(['To Do', 'In Progress', 'Done']):
            with cols[i]:
                st.markdown(f'<div class="sprint-column">', unsafe_allow_html=True)
                st.markdown(f"**{col_name}** ({len(st.session_state.sprint_board.get(col_name, []))})")
                
                # Display tasks
                for task in st.session_state.sprint_board.get(col_name, []):
                    st.markdown(f'''
                    <div class="task-item">
                        <strong>{task.get('task', 'Unknown task')}</strong><br>
                        <small>Added by: {task.get('user_id', 'Unknown')[:8]}</small>
                    </div>
                    ''', unsafe_allow_html=True)
                
                # Add new task
                with st.form(f"add_task_{col_name}"):
                    new_task = st.text_input(f"Add task to {col_name}", key=f"task_input_{col_name}")
                    if st.form_submit_button(f"➕ Add to {col_name}"):
                        if new_task and st.session_state.room_code:
                            try:
                                task_data = {
                                    "room_code": st.session_state.room_code,
                                    "column": col_name,
                                    "task": new_task,
                                    "user_id": st.session_state.user_id
                                }
                                result = api_post("/sprint/task", task_data)
                                if result:
                                    st.session_state.sprint_board[col_name].append(result)
                                    st.rerun()
                            except Exception as e:
                                st.error(f"Error adding task: {e}")
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with work_tab[1]:  # Meeting Notes
        st.markdown('<div class="work-card">', unsafe_allow_html=True)
        st.subheader("📝 Meeting Notes")
        
        # Load meeting notes from API
        if st.session_state.room_code:
            try:
                notes_data = api_get(f"/meeting/notes/{st.session_state.room_code}")
                if notes_data:
                    st.session_state.meeting_notes = notes_data.get("notes", "")
            except:
                pass
        
        # Meeting notes editor
        st.markdown('<div class="meeting-notes">', unsafe_allow_html=True)
        notes = st.text_area(
            "Shared Meeting Notes", 
            value=st.session_state.meeting_notes,
            height=300,
            placeholder="Add your meeting notes here...",
            key="meeting_notes_editor"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("💾 Save Notes"):
                if st.session_state.room_code:
                    try:
                        notes_data = {
                            "room_code": st.session_state.room_code,
                            "notes": notes,
                            "user_id": st.session_state.user_id
                        }
                        result = api_post("/meeting/notes", notes_data)
                        if result:
                            st.session_state.meeting_notes = notes
                            st.success("Notes saved!")
                    except Exception as e:
                        st.error(f"Error saving notes: {e}")
        
        with col2:
            st.markdown(f"**Last updated:** {datetime.now().strftime('%H:%M:%S')}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with work_tab[2]:  # Chat
        st.markdown('<div class="work-card">', unsafe_allow_html=True)
        st.subheader("💬 Chat")
        
        # Chat tabs
        chat_type = st.radio("Chat Type", ["Public", "Private"], horizontal=True, key="work_chat_type")
        
        if chat_type == "Public":
            render_chat_section()
        else:
            st.subheader("🔒 Private Chat")
            
            # User selection for private chat
            if st.session_state.room_code:
                try:
                    room_info = api_get(f"/rooms/{st.session_state.room_code}")
                    if room_info:
                        users = room_info.get('users', [])
                        # Filter out current user
                        other_users = [user for user in users if user != st.session_state.user_id]
                        
                        if other_users:
                            selected_user = st.selectbox(
                                "Select user to chat with:",
                                other_users,
                                format_func=lambda x: f"User {x[:8]}"
                            )
                            
                            # Load private messages
                            try:
                                private_messages = api_get(f"/chat/private/{st.session_state.user_id}/{selected_user}")
                                st.session_state.private_chats[f"{st.session_state.user_id}_{selected_user}"] = private_messages
                            except:
                                pass
                            
                            # Display private messages
                            chat_key = f"{st.session_state.user_id}_{selected_user}"
                            if chat_key in st.session_state.private_chats:
                                for msg in st.session_state.private_chats[chat_key][-20:]:
                                    is_sender = msg.get('sender_id') == st.session_state.user_id
                                    align = "right" if is_sender else "left"
                                    bg_color = "#007acc" if is_sender else "#e9ecef"
                                    text_color = "white" if is_sender else "black"
                                    
                                    st.markdown(f"""
                                    <div style="text-align: {align}; margin: 0.5rem 0;">
                                        <div style="
                                            background: {bg_color}; 
                                            color: {text_color}; 
                                            padding: 0.5rem 1rem; 
                                            border-radius: 15px; 
                                            display: inline-block; 
                                            max-width: 70%;
                                        ">
                                            <strong>{msg.get('sender_username', 'Unknown')}</strong><br>
                                            {msg.get('message', '')}
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            # Send private message
                            with st.form("private_chat_form"):
                                private_message = st.text_input("Type your private message...", key="private_message_input")
                                if st.form_submit_button("Send"):
                                    if private_message:
                                        try:
                                            message_data = {
                                                "sender_id": st.session_state.user_id,
                                                "receiver_id": selected_user,
                                                "sender_username": st.session_state.username,
                                                "message": private_message
                                            }
                                            result = api_post("/chat/private", message_data)
                                            if result:
                                                if chat_key not in st.session_state.private_chats:
                                                    st.session_state.private_chats[chat_key] = []
                                                st.session_state.private_chats[chat_key].append(result)
                                                st.rerun()
                                        except Exception as e:
                                            st.error(f"Error sending message: {e}")
                        else:
                            st.info("No other users in the room to chat with.")
                except Exception as e:
                    st.error(f"Error loading room users: {e}")
            else:
                st.info("Join a room to use private chat.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with work_tab[3]:  # Video Call
        st.markdown('<div class="work-card">', unsafe_allow_html=True)
        st.subheader("📹 Video Call")
        
        # Video call options
        call_type = st.radio("Call Type", ["Jitsi Meet", "Custom Room"], horizontal=True)
        
        if call_type == "Jitsi Meet":
            room_name = st.text_input("Meeting Room Name", value=f"PartyWatch-{st.session_state.room_code or 'Work'}")
            if st.button("🎥 Start Video Call"):
                jitsi_url = f"https://meet.jit.si/{room_name.replace(' ', '')}"
                st.markdown(f"""
                <iframe 
                    src="{jitsi_url}" 
                    width="100%" 
                    height="500" 
                    allow="camera; microphone; fullscreen; display-capture"
                    style="border-radius: 8px;"
                ></iframe>
                """, unsafe_allow_html=True)
                st.info(f"Meeting URL: {jitsi_url}")
        else:
            st.info("Custom video call integration coming soon...")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with work_tab[4]:  # Settings
        st.markdown('<div class="work-card">', unsafe_allow_html=True)
        st.subheader("⚙️ Work Mode Settings")
        
        # Professional settings
        st.checkbox("Enable notifications", value=True, key="work_notifications")
        st.checkbox("Auto-save notes", value=True, key="auto_save_notes")
        st.checkbox("Show task timestamps", value=True, key="show_timestamps")
        
        # Sprint settings
        st.subheader("Sprint Settings")
        sprint_duration = st.selectbox("Sprint Duration", ["1 week", "2 weeks", "3 weeks", "4 weeks"])
        st.date_input("Sprint Start Date", key="sprint_start_date")
        st.date_input("Sprint End Date", key="sprint_end_date")
        
        # Export options
        st.subheader("Export Options")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Export Sprint Report"):
                st.info("Sprint report export coming soon...")
        with col2:
            if st.button("📝 Export Meeting Notes"):
                st.info("Meeting notes export coming soon...")
        
        st.markdown('</div>', unsafe_allow_html=True)

def sidebar_room_settings():
    st.header("🏠 Room Management")
    room_type = st.radio("Room Type", ["YouTube", "Spotify", "Screenshare"], index=["YouTube", "Spotify", "Screenshare"].index(st.session_state.room_type) if 'room_type' in st.session_state else 0)
    st.session_state.room_type = room_type
    st.session_state.room_desc = st.text_input("Room Description (optional)", value=st.session_state.room_desc)
    st.session_state.room_is_public = st.checkbox("Public Room", value=st.session_state.room_is_public)
    st.session_state.room_password = st.text_input("Room Password (optional)", value=st.session_state.room_password, type="password")

def update_room_state():
    """
    Periodically fetches state from the backend.
    - Chat messages are fetched frequently (differential update).
    - General room info is fetched less frequently.
    """
    if not st.session_state.get("room_code"):
        return

    st.session_state.poll_counter = st.session_state.get('poll_counter', 0) + 1

    try:
        # --- Fast Polling: Chat Messages (every ~3 seconds) ---
        last_timestamp = "1970-01-01T00:00:00.000000"
        if st.session_state.chat_messages:
            last_timestamp = st.session_state.chat_messages[-1]['timestamp']
        
        # For this to be efficient, the backend API must support the `since` parameter
        # to return only new messages. Otherwise, it will re-send the full history.
        new_messages = api_get(f"/chat/{st.session_state.room_code}/messages?since={last_timestamp}")
        
        if new_messages:
            st.session_state.chat_messages.extend(new_messages)
            st.session_state.unread_count += len(new_messages)

        # --- Slow Polling: General Room Info (every 4th poll, i.e., ~12 seconds) ---
        if st.session_state.poll_counter % 4 == 0:
            room_info = api_get(f"/rooms/{st.session_state.room_code}")
            if room_info:
                # Check for host promotion
                was_host = st.session_state.is_host
                is_now_host = st.session_state.user_id == room_info.get('host_id')
                if is_now_host and not was_host:
                    st.toast("👑 You have been promoted to room host!", icon="🎉")

                st.session_state.is_host = is_now_host
                st.session_state.room_info = room_info
                st.session_state.room_desc = room_info.get("room_desc", st.session_state.get("room_desc", ""))
            
    except requests.RequestException:
        # Fail silently if the backend is temporarily unavailable during a poll
        pass
    except Exception:
        # Could log this for debugging, but don't show UI error on a poll
        pass

def main():
    theme_toggle()
    st.markdown('<h1 class="main-header">🎬 PartyWatch</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem;">Create and join shared YouTube, Spotify, or Screenshare rooms with real-time chat and presence</p>', unsafe_allow_html=True)
    
    with st.sidebar:
        avatar_selector()
        sidebar_room_settings()
        mode = st.radio("Choose Mode", ["Party", "Work"], key="mode_toggle")
        st.session_state.mode = mode
        
        # Work Mode Logic
        if st.session_state.mode == "Work":
            work_mode_ui()
            st.stop()  # Stop further rendering in Work mode
        
        if st.session_state.room_code:
            st.success(f"Connected to room: **{st.session_state.room_code}**")
            invite_link(st.session_state.room_code)
            if st.session_state.is_host:
                st.info("You are the host")
            else:
                st.info("You are a viewer")
            if st.button("Show Profile"):
                st.session_state.show_profile = True
            if st.button("Leave Room"):
                try:
                    # Notify the backend that this user is leaving.
                    # This allows the backend to handle host migration if needed.
                    api_post(f"/rooms/{st.session_state.room_code}/leave", {"user_id": st.session_state.user_id})
                except Exception as e:
                    # Even if the API call fails, the user should be able to leave the UI.
                    # This could be logged to a more persistent store for debugging.
                    print(f"Could not notify backend of leave action: {e}")
                finally:
                    # Reset local session state to leave the room UI
                    st.session_state.room_code = None
                    st.session_state.is_host = False
                    st.session_state.current_video_id = None
                    st.session_state.current_spotify_type = None
                    st.session_state.current_spotify_id = None
                    st.session_state.playback_state = {'playing': False, 'current_time': 0}
                    st.session_state.chat_messages = []
                    st.rerun()
        else:
            if st.session_state.room_type == "YouTube":
                st.subheader("Create YouTube Room")
                with st.form("create_room_form"):
                    video_url = st.text_input("YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")
                    room_name = st.text_input("Your Name", value=st.session_state.username)
                    create_button = st.form_submit_button("Create Room")
                    if create_button and video_url and room_name:
                        with st.spinner("Creating your room..."):
                            # Sanitize username before sending to backend
                            safe_username = sanitize_input(room_name)
                            if not safe_username:
                                st.warning("Please enter a valid name.")
                            else:
                                room_code = create_room(video_url, safe_username)
                                if room_code:
                                    st.success(f"Room created! Code: **{room_code}**")
                                    st.rerun()
                st.divider()
                join_room_ui()
            elif st.session_state.room_type == "Spotify":
                st.subheader("Create Spotify Room")
                with st.form("create_spotify_room_form"):
                    spotify_url = st.text_input("Spotify Track/Playlist/Album URL", placeholder="https://open.spotify.com/track/... or playlist/... or album/...")
                    room_name = st.text_input("Your Name", value=st.session_state.username, key="spotify_room_name")
                    create_button = st.form_submit_button("Create Spotify Room")
                    if create_button and spotify_url and room_name:
                        with st.spinner("Creating Spotify room..."):
                            # Sanitize username before sending to backend
                            safe_username = sanitize_input(room_name)
                            if not safe_username:
                                st.warning("Please enter a valid name.")
                            else:
                                room_code = create_spotify_room(spotify_url, safe_username)
                                if room_code:
                                    st.success(f"Spotify Room created! Code: **{room_code}**")
                                    st.rerun()
                st.divider()
                st.subheader("Join Spotify Room")
                join_room_ui()
            else:  # Screenshare
                st.subheader("Create Screenshare Room")
                with st.form("create_screenshare_room_form"):
                    room_name = st.text_input("Your Name", value=st.session_state.username, key="screenshare_room_name")
                    create_button = st.form_submit_button("Create Screenshare Room")
                    if create_button and room_name:
                        with st.spinner("Creating screenshare room..."):
                            # Sanitize username before sending to backend
                            safe_username = sanitize_input(room_name)
                            if not safe_username:
                                st.warning("Please enter a valid name.")
                                return

                            room_code = str(uuid.uuid4())[:8].upper()
                            room_data = {
                                "room_code": room_code,
                                "host_id": st.session_state.user_id,
                                "room_name": safe_username,
                                "room_type": "Screenshare"
                            }
                            result = api_post("/rooms", room_data)
                            if result:
                                st.session_state.room_code = room_code
                                st.session_state.is_host = True
                                st.session_state.username = safe_username
                                st.session_state.room_type = 'Screenshare'
                                st.session_state.room_desc = "Screensharing Room"
                                st.session_state.room_is_public = True
                                st.session_state.room_password = None
                                st.markdown('<script>window.confettiBurst && window.confettiBurst();</script>', unsafe_allow_html=True)
                                st.rerun()
                st.divider()
                st.subheader("Join Screenshare Room")
                join_room_ui()
    
    if st.session_state.show_profile:
        user_profile()
        return
    
    if st.session_state.room_code:
        st.markdown(f"""
        <div class="room-card">
            <h3>Room: {st.session_state.room_code}</h3>
            <p>{st.session_state.room_desc}</p>
            <p>Host: {st.session_state.username if st.session_state.is_host else 'Unknown'}</p>
            <p>{'🔓 Public' if st.session_state.room_is_public else '🔒 Private'}{' | Password set' if st.session_state.room_password else ''}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.session_state.room_type == "YouTube":
                if st.session_state.current_video_id:
                    render_youtube_player(st.session_state.current_video_id, st.session_state.is_host)
                else:
                    st.warning("No video loaded in this room")
            elif st.session_state.room_type == "Spotify":
                render_spotify_embed(st.session_state.current_spotify_type, st.session_state.current_spotify_id)
            else:  # Screenshare
                st.subheader("🖥️ Screensharing (Beta)")
                screenshare_role = st.radio("Choose your role", ["Host (share screen)", "Viewer (watch screen)"], horizontal=True, key="screenshare_role_radio")
                st.session_state.screenshare_role = screenshare_role
                if screenshare_role == "Host (share screen)":
                    webrtc_streamer(
                        key="screenshare",
                        mode="sendonly",
                        media_stream_constraints={
                            "video": True,
                            "audio": False,
                            "video": {"mediaSource": "screen"}
                        },
                        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
                    )
                else:
                    webrtc_streamer(
                        key="screenshare",
                        mode="recvonly",
                        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
                    )
            poll_widget()
            queue_widget()
        
        with col2:
            render_user_presence()
            render_chat_section()
        
        # This polling loop is a simple way to keep the app updated
        # with new messages and user statuses from the backend.
        update_room_state()
        time.sleep(3)
        st.rerun()
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem;">
            <h2>Welcome to PartyWatch! 🎉</h2>
            <p style="font-size: 1.1rem; margin: 2rem 0;">
                Create a new room to start watching YouTube videos, listening to Spotify, or sharing your screen with friends, or join an existing room using a room code.
            </p>
            <div style="
                background: rgba(255,255,255,0.92);
                padding: 2.5rem 2rem 2rem 2rem;
                border-radius: 18px;
                margin: 2rem auto;
                max-width: 600px;
                box-shadow: 0 8px 32px 0 rgba(31,38,135,0.18);
                border: 1.5px solid #e0e0e0;
            ">
                <div style="font-size:2.2rem; font-weight:900; color:#00ffe7; letter-spacing:1px; margin-bottom:0.5rem;">
                    ✨ <span style="background: linear-gradient(90deg,#00ffe7,#ff6bcb); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Features:</span>
                </div>
                <ul style="text-align:left; display:inline-block; font-size:1.25rem; color:#222; font-weight:600; line-height:2;">
                    <li>Real-time video synchronization (YouTube)</li>
                    <li>Spotify listening parties (Premium users get full playback)</li>
                    <li>Screensharing for any content (host shares, others watch)</li>
                    <li>Host-only playback controls (YouTube)</li>
                    <li>Live chat with room members</li>
                    <li>User presence indicators</li>
                    <li>Unique room codes for easy sharing</li>
                    <li>Emoji reactions, GIFs, polls, queue, and more!</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 