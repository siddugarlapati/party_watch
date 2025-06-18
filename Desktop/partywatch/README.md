# 🎬 PartyWatch - Shared YouTube Watch Rooms

A Streamlit-based web application that allows users to create and join shared watch rooms for YouTube videos with real-time synchronization, chat, and user presence features.

## ✨ Features

- **🎥 Full YouTube Player Integration**: Embedded YouTube player with host controls
- **🔄 Real-time Synchronization**: Playback state sync across all participants
- **👑 Host Controls**: Play, pause, and seek controls for room hosts
- **💬 Live Chat**: Real-time chat with room members
- **👥 User Presence**: See who's in the room with online indicators
- **🔐 Unique Room Codes**: Easy room sharing with 8-character codes
- **📱 Responsive Design**: Clean, modern UI that works on all devices
- **🔌 WebSocket Support**: Real-time communication between participants
- **🔥 Firebase Integration**: Optional Firebase Realtime Database for persistence

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd partywatch
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 🛠️ Configuration

### Firebase Setup (Optional)

For enhanced real-time features and data persistence, you can set up Firebase:

1. **Create a Firebase project** at [Firebase Console](https://console.firebase.google.com/)

2. **Enable Realtime Database** in your Firebase project

3. **Download service account key**:
   - Go to Project Settings > Service Accounts
   - Click "Generate new private key"
   - Save the JSON file securely

4. **Set environment variables**:
   ```bash
   # Create a .env file
   FIREBASE_SERVICE_ACCOUNT_PATH=path/to/your/serviceAccountKey.json
   FIREBASE_DATABASE_URL=https://your-project-id.firebaseio.com/
   ```

### WebSocket Server (Optional)

For real-time communication, you can run the WebSocket server:

```bash
python websocket_server.py
```

The WebSocket server runs on `ws://localhost:8765` by default.

## 📖 Usage Guide

### Creating a Room

1. **Enter YouTube URL**: Paste a valid YouTube video URL
2. **Enter your name**: Choose a display name for the room
3. **Click "Create Room"**: A unique 8-character room code will be generated
4. **Share the code**: Send the room code to friends to join

### Joining a Room

1. **Enter room code**: Input the 8-character room code provided by the host
2. **Enter your name**: Choose your display name
3. **Click "Join Room"**: You'll be connected to the room

### Host Controls

As the room host, you can:
- **Play/Pause**: Control video playback for all participants
- **Seek**: Jump to specific timestamps in the video
- **Sync**: Ensure all participants are watching the same part

### Chat Features

- **Send messages**: Type in the chat box and press Enter
- **Real-time updates**: See messages from all room members instantly
- **User indicators**: See who sent each message

### User Presence

- **Online indicators**: Green dots show who's currently in the room
- **Host badge**: The room creator is marked as "HOST"
- **Real-time updates**: See when users join or leave

## 🏗️ Architecture

### Components

- **`app.py`**: Main Streamlit application
- **`websocket_server.py`**: WebSocket server for real-time communication
- **`firebase_config.py`**: Firebase integration and database operations
- **`requirements.txt`**: Python dependencies

### Data Flow

1. **Room Creation**: Host creates room with YouTube URL
2. **User Joining**: Participants join using room code
3. **Real-time Sync**: WebSocket/Firebase handles state synchronization
4. **Playback Control**: Host controls are broadcast to all participants
5. **Chat**: Messages are sent through real-time channels

## 🔧 Customization

### Adding New Features

The modular architecture makes it easy to add new features:

1. **New video platforms**: Extend the video player integration
2. **Additional controls**: Add more host controls in `app.py`
3. **Enhanced chat**: Add emojis, file sharing, or voice messages
4. **Room settings**: Add room customization options

### Styling

Customize the appearance by modifying the CSS in `app.py`:

```python
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF6B6B;
    }
    /* Add your custom styles here */
</style>
""", unsafe_allow_html=True)
```

## 🐛 Troubleshooting

### Common Issues

1. **YouTube player not loading**:
   - Check if the YouTube URL is valid
   - Ensure the video is not age-restricted or private

2. **Real-time features not working**:
   - Verify WebSocket server is running
   - Check Firebase configuration if using Firebase

3. **Room not found**:
   - Verify the room code is correct (8 characters, case-sensitive)
   - Check if the room was created recently

4. **Chat not updating**:
   - Refresh the page
   - Check browser console for errors

### Debug Mode

Enable debug mode by setting:

```python
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web app framework
- [YouTube Data API](https://developers.google.com/youtube/v3) for video integration
- [Firebase](https://firebase.google.com/) for real-time database features
- [WebSockets](https://websockets.readthedocs.io/) for real-time communication

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-repo/partywatch/issues) page
2. Create a new issue with detailed information
3. Include your Python version, OS, and error messages

---

**Happy watching together! 🎬✨** 