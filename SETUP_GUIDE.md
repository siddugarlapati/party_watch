# 🚀 PartyWatch Quick Setup Guide

## What We Built

PartyWatch is a complete Streamlit-based web application for creating and joining shared YouTube watch rooms with real-time synchronization. Here's what's included:

### 🎯 Core Features
- ✅ **Full YouTube Player Integration** - Embedded player with host controls
- ✅ **Real-time Synchronization** - Playback sync across all participants  
- ✅ **Host Controls** - Play, pause, and seek for room hosts
- ✅ **Live Chat** - Real-time chat with room members
- ✅ **User Presence** - See who's online with indicators
- ✅ **Unique Room Codes** - 8-character codes for easy sharing
- ✅ **Responsive Design** - Clean, modern UI for all devices
- ✅ **WebSocket Support** - Real-time communication
- ✅ **Firebase Integration** - Optional database for persistence

### 📁 Project Structure
```
partywatch/
├── app.py                 # Main Streamlit application
├── websocket_server.py    # WebSocket server for real-time sync
├── firebase_config.py     # Firebase integration
├── utils.py              # Utility functions
├── config.py             # Application configuration
├── run.py                # Startup script
├── requirements.txt      # Python dependencies
├── README.md             # Comprehensive documentation
├── env_example.txt       # Environment variables template
└── SETUP_GUIDE.md        # This file
```

## 🚀 Quick Start (3 Steps)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
# Option A: Use the startup script
python run.py

# Option B: Run directly
streamlit run app.py
```

### 3. Open Your Browser
Navigate to: `http://localhost:8501`

## 🎬 How to Use

### Creating a Room
1. Enter a YouTube video URL
2. Enter your name
3. Click "Create Room"
4. Share the 8-character room code with friends

### Joining a Room
1. Enter the room code provided by the host
2. Enter your name
3. Click "Join Room"

### Host Controls
- **Play/Pause**: Control video for all participants
- **Seek**: Jump to specific timestamps
- **Sync**: Keep everyone on the same part

### Chat Features
- Send real-time messages
- See user indicators
- View message timestamps

## 🔧 Advanced Setup

### Firebase Integration (Optional)
1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Enable Realtime Database
3. Download service account key
4. Create `.env` file with your credentials:
```bash
FIREBASE_SERVICE_ACCOUNT_PATH=path/to/serviceAccountKey.json
FIREBASE_DATABASE_URL=https://your-project.firebaseio.com/
```

### WebSocket Server (Optional)
For enhanced real-time features:
```bash
python websocket_server.py
```

## 🎯 Key Components Explained

### `app.py` - Main Application
- Streamlit UI with room creation/joining
- YouTube player embedding
- Real-time chat interface
- User presence indicators
- Host controls for playback

### `websocket_server.py` - Real-time Communication
- WebSocket server for instant messaging
- Room state synchronization
- User presence tracking
- Playback state broadcasting

### `firebase_config.py` - Database Operations
- Firebase Realtime Database integration
- Room data persistence
- User management
- Chat message storage

### `utils.py` - Helper Functions
- Video ID extraction from URLs
- Input validation and sanitization
- Time formatting utilities
- Security functions

### `config.py` - Application Settings
- Feature flags and configuration
- Error messages and validation
- Rate limiting and caching
- UI theme colors

## 🐛 Troubleshooting

### Common Issues
1. **YouTube player not loading**: Check URL validity
2. **Real-time features not working**: Ensure WebSocket server is running
3. **Room not found**: Verify room code (8 characters, case-sensitive)
4. **Dependencies missing**: Run `pip install -r requirements.txt`

### Debug Mode
Enable debug logging in `config.py`:
```python
DEBUG_MODE = True
```

## 🎨 Customization

### Adding New Features
The modular architecture makes it easy to extend:
- New video platforms in `utils.py`
- Additional controls in `app.py`
- Enhanced chat features
- Custom UI themes

### Styling
Modify CSS in `app.py`:
```python
st.markdown("""
<style>
    .main-header {
        color: #FF6B6B;
        font-size: 3rem;
    }
</style>
""", unsafe_allow_html=True)
```

## 📱 Browser Compatibility
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

## 🔒 Security Notes
- Room codes are randomly generated
- User input is sanitized
- Rate limiting prevents spam
- Session management included

## 🚀 Deployment Options
- **Local Development**: `streamlit run app.py`
- **Cloud Platforms**: Streamlit Cloud, Heroku, AWS
- **Docker**: Containerized deployment
- **Production**: Add SSL, load balancing, monitoring

---

## 🎉 You're Ready!

Your PartyWatch application is now running and ready to use! 

**Next Steps:**
1. Test creating a room with a YouTube URL
2. Share the room code with friends
3. Try the host controls and chat features
4. Customize the UI and add new features

**Happy watching together! 🎬✨** 