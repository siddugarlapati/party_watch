import streamlit as st
import uuid
import json
import time
from datetime import datetime
import requests
import os

# Configure for Streamlit Cloud
st.set_page_config(
    page_title="PartyWatch - Shared Watch Rooms",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend URL - will be set by environment variable in deployment
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api")

# API functions
def api_post(path, data):
    """Make POST request to backend API"""
    try:
        response = requests.post(f"{BACKEND_URL}{path}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Fallback to local storage if backend is not available
        return None

def api_get(path):
    """Make GET request to backend API"""
    try:
        response = requests.get(f"{BACKEND_URL}{path}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Fallback to local storage if backend is not available
        return None

# Session state initialization
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if 'room_code' not in st.session_state:
    st.session_state.room_code = None
if 'is_host' not in st.session_state:
    st.session_state.is_host = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'room_type' not in st.session_state:
    st.session_state.room_type = 'YouTube'
if 'video_id' not in st.session_state:
    st.session_state.video_id = None
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'room_users' not in st.session_state:
    st.session_state.room_users = []
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
    st.session_state.sprint_board = {
        "To Do": [],
        "In Progress": [],
        "Done": []
    }
if 'meeting_notes' not in st.session_state:
    st.session_state.meeting_notes = ""
if 'rooms' not in st.session_state:
    st.session_state.rooms = {}

# Work mode UI
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
        
        # Load sprint board from API if backend is available
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
                        if new_task:
                            task = {
                                "id": str(uuid.uuid4()),
                                "task": new_task,
                                "user_id": st.session_state.user_id,
                                "created_at": datetime.now().isoformat()
                            }
                            
                            # Try to save to backend first
                            if st.session_state.room_code:
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
                                    else:
                                        st.session_state.sprint_board[col_name].append(task)
                                except:
                                    st.session_state.sprint_board[col_name].append(task)
                            else:
                                st.session_state.sprint_board[col_name].append(task)
                            
                            st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with work_tab[1]:  # Meeting Notes
        st.markdown('<div class="work-card">', unsafe_allow_html=True)
        st.subheader("📝 Meeting Notes")
        
        # Load meeting notes from API if backend is available
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
                st.session_state.meeting_notes = notes
                
                # Try to save to backend
                if st.session_state.room_code:
                    try:
                        notes_data = {
                            "room_code": st.session_state.room_code,
                            "notes": notes,
                            "user_id": st.session_state.user_id
                        }
                        result = api_post("/meeting/notes", notes_data)
                        if result:
                            st.success("Notes saved to cloud!")
                        else:
                            st.success("Notes saved locally!")
                    except:
                        st.success("Notes saved locally!")
                else:
                    st.success("Notes saved!")
        
        with col2:
            st.markdown(f"**Last updated:** {datetime.now().strftime('%H:%M:%S')}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with work_tab[2]:  # Chat
        st.markdown('<div class="work-card">', unsafe_allow_html=True)
        st.subheader("💬 Chat")
        
        # Load chat messages from API if backend is available
        if st.session_state.room_code:
            try:
                chat_data = api_get(f"/chat/{st.session_state.room_code}/messages")
                if chat_data:
                    st.session_state.chat_messages = chat_data
            except:
                pass
        
        # Simple chat interface
        chat_message = st.text_input("Type your message...", key="work_chat_input")
        if st.button("Send"):
            if chat_message:
                msg = {
                    "id": str(uuid.uuid4()),
                    "user_id": st.session_state.user_id,
                    "username": st.session_state.username or "Anonymous",
                    "message": chat_message,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Try to save to backend
                if st.session_state.room_code:
                    try:
                        chat_data = {
                            "room_code": st.session_state.room_code,
                            "user_id": st.session_state.user_id,
                            "username": st.session_state.username or "Anonymous",
                            "message": chat_message
                        }
                        result = api_post("/chat/messages", chat_data)
                        if result:
                            st.session_state.chat_messages.append(result)
                        else:
                            st.session_state.chat_messages.append(msg)
                    except:
                        st.session_state.chat_messages.append(msg)
                else:
                    st.session_state.chat_messages.append(msg)
                
                st.rerun()
        
        # Display messages
        for msg in st.session_state.chat_messages[-20:]:
            st.markdown(f"""
            <div style="background: #e9ecef; padding: 0.5rem; margin: 0.5rem 0; border-radius: 8px;">
                <strong>{msg.get('username', 'Unknown')}</strong>: {msg.get('message', '')}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with work_tab[3]:  # Video Call
        st.markdown('<div class="work-card">', unsafe_allow_html=True)
        st.subheader("📹 Video Call")
        
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
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with work_tab[4]:  # Settings
        st.markdown('<div class="work-card">', unsafe_allow_html=True)
        st.subheader("⚙️ Work Mode Settings")
        
        st.checkbox("Enable notifications", value=True, key="work_notifications")
        st.checkbox("Auto-save notes", value=True, key="auto_save_notes")
        st.checkbox("Show task timestamps", value=True, key="show_timestamps")
        
        st.subheader("Sprint Settings")
        sprint_duration = st.selectbox("Sprint Duration", ["1 week", "2 weeks", "3 weeks", "4 weeks"])
        st.date_input("Sprint Start Date", key="sprint_start_date")
        st.date_input("Sprint End Date", key="sprint_end_date")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Main app
def main():
    st.markdown('<h1 class="main-header">🎬 PartyWatch</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem;">Create and join shared YouTube, Spotify, or Screenshare rooms with real-time chat and presence</p>', unsafe_allow_html=True)
    
    with st.sidebar:
        # Mode toggle
        mode = st.radio("Choose Mode", ["Party", "Work"], key="mode_toggle")
        st.session_state.mode = mode
        
        # Work Mode Logic
        if st.session_state.mode == "Work":
            work_mode_ui()
            st.stop()
        
        # Party mode logic
        st.subheader("Create Room")
        room_type = st.radio("Room Type", ["YouTube", "Spotify", "Screenshare"])
        
        if room_type == "YouTube":
            with st.form("create_youtube_room"):
                video_url = st.text_input("YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")
                room_name = st.text_input("Your Name", value=st.session_state.username)
                create_button = st.form_submit_button("Create YouTube Room")
                if create_button and video_url and room_name:
                    room_code = str(uuid.uuid4())[:8].upper()
                    
                    # Try to create room in backend
                    try:
                        room_data = {
                            "room_code": room_code,
                            "host_id": st.session_state.user_id,
                            "video_id": video_url.split("v=")[1] if "v=" in video_url else None,
                            "room_name": room_name,
                            "room_type": "YouTube"
                        }
                        result = api_post("/rooms", room_data)
                        if result:
                            st.success("Room created in cloud!")
                        else:
                            st.success("Room created locally!")
                    except:
                        st.success("Room created locally!")
                    
                    st.session_state.room_code = room_code
                    st.session_state.is_host = True
                    st.session_state.username = room_name
                    st.session_state.room_type = 'YouTube'
                    st.session_state.video_id = video_url.split("v=")[1] if "v=" in video_url else None
                    st.rerun()
        
        elif room_type == "Spotify":
            with st.form("create_spotify_room"):
                spotify_url = st.text_input("Spotify URL", placeholder="https://open.spotify.com/track/...")
                room_name = st.text_input("Your Name", value=st.session_state.username)
                create_button = st.form_submit_button("Create Spotify Room")
                if create_button and spotify_url and room_name:
                    room_code = str(uuid.uuid4())[:8].upper()
                    
                    # Try to create room in backend
                    try:
                        room_data = {
                            "room_code": room_code,
                            "host_id": st.session_state.user_id,
                            "spotify_url": spotify_url,
                            "room_name": room_name,
                            "room_type": "Spotify"
                        }
                        result = api_post("/rooms", room_data)
                        if result:
                            st.success("Room created in cloud!")
                        else:
                            st.success("Room created locally!")
                    except:
                        st.success("Room created locally!")
                    
                    st.session_state.room_code = room_code
                    st.session_state.is_host = True
                    st.session_state.username = room_name
                    st.session_state.room_type = 'Spotify'
                    st.rerun()
        
        else:  # Screenshare
            with st.form("create_screenshare_room"):
                room_name = st.text_input("Your Name", value=st.session_state.username)
                create_button = st.form_submit_button("Create Screenshare Room")
                if create_button and room_name:
                    room_code = str(uuid.uuid4())[:8].upper()
                    
                    # Try to create room in backend
                    try:
                        room_data = {
                            "room_code": room_code,
                            "host_id": st.session_state.user_id,
                            "room_name": room_name,
                            "room_type": "Screenshare"
                        }
                        result = api_post("/rooms", room_data)
                        if result:
                            st.success("Room created in cloud!")
                        else:
                            st.success("Room created locally!")
                    except:
                        st.success("Room created locally!")
                    
                    st.session_state.room_code = room_code
                    st.session_state.is_host = True
                    st.session_state.username = room_name
                    st.session_state.room_type = 'Screenshare'
                    st.rerun()
        
        st.divider()
        st.subheader("Join Room")
        with st.form("join_room"):
            join_code = st.text_input("Room Code", placeholder="Enter 8-character code")
            join_name = st.text_input("Your Name")
            join_button = st.form_submit_button("Join Room")
            if join_button and join_code and join_name:
                # Try to join room in backend
                try:
                    join_data = {
                        "user_id": st.session_state.user_id,
                        "username": join_name
                    }
                    result = api_post(f"/rooms/{join_code.upper()}/join", join_data)
                    if result:
                        st.success("Successfully joined room in cloud!")
                    else:
                        st.success("Successfully joined room locally!")
                except:
                    st.success("Successfully joined room locally!")
                
                st.session_state.room_code = join_code.upper()
                st.session_state.is_host = False
                st.session_state.username = join_name
                st.rerun()
    
    # Main content area
    if st.session_state.room_code:
        st.success(f"Connected to room: **{st.session_state.room_code}**")
        
        # Room info
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
            <h3>Room: {st.session_state.room_code}</h3>
            <p>Type: {st.session_state.room_type}</p>
            <p>Host: {st.session_state.username if st.session_state.is_host else 'Unknown'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Content based on room type
        if st.session_state.room_type == "YouTube":
            st.subheader("🎬 YouTube Player")
            
            # YouTube player with real-time sync
            if st.session_state.room_code:
                # Get video ID from room data
                video_id = None
                if st.session_state.is_host:
                    # For host, get from session state
                    video_id = st.session_state.video_id
                else:
                    # For guests, try to get from backend
                    try:
                        room_data = api_get(f"/rooms/{st.session_state.room_code}")
                        if room_data:
                            video_id = room_data.get('video_id')
                    except:
                        pass
                
                if video_id:
                    # YouTube embed with controls
                    st.markdown(f"""
                    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                        <iframe 
                            src="https://www.youtube.com/embed/{video_id}?enablejsapi=1&origin={st.experimental_get_query_params().get('origin', [''])[0]}" 
                            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" 
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                            allowfullscreen>
                        </iframe>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Video controls
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("⏮️ Previous"):
                            st.info("Previous video feature coming soon...")
                    with col2:
                        if st.button("⏸️ Pause/Play"):
                            st.info("Video control sync coming soon...")
                    with col3:
                        if st.button("⏭️ Next"):
                            st.info("Next video feature coming soon...")
                    
                    # Video URL display
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                        <strong>Current Video:</strong> https://www.youtube.com/watch?v={video_id}
                    </div>
                    """, unsafe_allow_html=True)
                    
                else:
                    st.warning("No video loaded. Host needs to add a YouTube URL.")
                    
                    # For host, allow changing video
                    if st.session_state.is_host:
                        with st.expander("🎬 Change Video"):
                            new_video_url = st.text_input("New YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
                            if st.button("Change Video"):
                                if new_video_url and "youtube.com" in new_video_url:
                                    # Extract video ID
                                    if "v=" in new_video_url:
                                        new_video_id = new_video_url.split("v=")[1].split("&")[0]
                                        
                                        # Update in backend
                                        try:
                                            update_data = {
                                                "video_id": new_video_id
                                            }
                                            result = api_post(f"/rooms/{st.session_state.room_code}/update", update_data)
                                            if result:
                                                st.success("Video updated in cloud!")
                                            else:
                                                st.success("Video updated locally!")
                                        except:
                                            st.success("Video updated locally!")
                                        
                                        st.session_state.video_id = new_video_id
                                        st.rerun()
                                    else:
                                        st.error("Invalid YouTube URL")
                                else:
                                    st.error("Please enter a valid YouTube URL")
            else:
                st.info("Join a room to start watching!")
        
        elif st.session_state.room_type == "Spotify":
            st.subheader("🎵 Spotify Player")
            st.info("Spotify player integration coming soon...")
        
        else:  # Screenshare
            st.subheader("🖥️ Screensharing")
            st.info("Screensharing integration coming soon...")
        
        # Chat section
        st.subheader("💬 Chat")
        chat_message = st.text_input("Type your message...", key="chat_input")
        if st.button("Send"):
            if chat_message:
                msg = {
                    "id": str(uuid.uuid4()),
                    "user_id": st.session_state.user_id,
                    "username": st.session_state.username or "Anonymous",
                    "message": chat_message,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Try to save to backend
                if st.session_state.room_code:
                    try:
                        chat_data = {
                            "room_code": st.session_state.room_code,
                            "user_id": st.session_state.user_id,
                            "username": st.session_state.username or "Anonymous",
                            "message": chat_message
                        }
                        result = api_post("/chat/messages", chat_data)
                        if result:
                            st.session_state.chat_messages.append(result)
                        else:
                            st.session_state.chat_messages.append(msg)
                    except:
                        st.session_state.chat_messages.append(msg)
                else:
                    st.session_state.chat_messages.append(msg)
                
                st.rerun()
        
        # Display messages
        for msg in st.session_state.chat_messages[-20:]:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 0.5rem; margin: 0.5rem 0; border-radius: 8px;">
                <strong>{msg.get('username', 'Unknown')}</strong>: {msg.get('message', '')}
            </div>
            """, unsafe_allow_html=True)
        
        # Leave room button
        if st.button("Leave Room"):
            st.session_state.room_code = None
            st.session_state.is_host = False
            st.rerun()
    
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem;">
            <h2>Welcome to PartyWatch! 🎉</h2>
            <p style="font-size: 1.1rem; margin: 2rem 0;">
                Create a new room to start watching YouTube videos, listening to Spotify, or sharing your screen with friends, or join an existing room using a room code.
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 