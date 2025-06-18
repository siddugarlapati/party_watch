"""
PartyWatch Configuration
Application settings and constants
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application Settings
APP_NAME = "PartyWatch"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Shared YouTube Watch Rooms with Real-time Synchronization"

# Server Configuration
STREAMLIT_PORT = int(os.getenv('STREAMLIT_SERVER_PORT', 8501))
STREAMLIT_HOST = os.getenv('STREAMLIT_SERVER_ADDRESS', 'localhost')
WEBSOCKET_PORT = int(os.getenv('WEBSOCKET_PORT', 8765))
WEBSOCKET_HOST = os.getenv('WEBSOCKET_HOST', 'localhost')

# Firebase Configuration
FIREBASE_ENABLED = os.getenv('FIREBASE_ENABLED', 'false').lower() == 'true'
FIREBASE_SERVICE_ACCOUNT_PATH = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH')
FIREBASE_DATABASE_URL = os.getenv('FIREBASE_DATABASE_URL')
FIREBASE_CONFIG = os.getenv('FIREBASE_CONFIG')

# Room Configuration
ROOM_CODE_LENGTH = 8
MAX_ROOM_NAME_LENGTH = 50
MAX_USERNAME_LENGTH = 20
MAX_CHAT_MESSAGE_LENGTH = 500
MAX_ROOM_USERS = 50
ROOM_CLEANUP_HOURS = 24

# Video Configuration
SUPPORTED_VIDEO_PLATFORMS = ['youtube']
MAX_VIDEO_DURATION = 7200  # 2 hours in seconds
DEFAULT_VIDEO_QUALITY = 'medium'

# Chat Configuration
MAX_CHAT_MESSAGES_PER_ROOM = 100
CHAT_MESSAGE_RATE_LIMIT = 5  # messages per minute per user

# Security Configuration
SESSION_TIMEOUT_MINUTES = 60
MAX_LOGIN_ATTEMPTS = 5
PASSWORD_MIN_LENGTH = 6

# UI Configuration
THEME_COLORS = {
    'primary': '#FF6B6B',
    'secondary': '#4ECDC4',
    'accent': '#45B7D1',
    'success': '#96CEB4',
    'warning': '#FFEAA7',
    'error': '#DDA0A0',
    'background': '#F7F7F7',
    'text': '#2C3E50'
}

# YouTube Configuration
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_EMBED_URL = "https://www.youtube.com/embed/{video_id}?enablejsapi=1&origin={origin}"

# WebSocket Configuration
WEBSOCKET_PING_INTERVAL = 30  # seconds
WEBSOCKET_PING_TIMEOUT = 10   # seconds
WEBSOCKET_MAX_MESSAGE_SIZE = 1024 * 1024  # 1MB

# Development Configuration
DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Feature Flags
ENABLE_FIREBASE = FIREBASE_ENABLED
ENABLE_WEBSOCKET = True
ENABLE_CHAT = True
ENABLE_USER_PRESENCE = True
ENABLE_HOST_CONTROLS = True
ENABLE_VIDEO_INFO = True

# Error Messages
ERROR_MESSAGES = {
    'invalid_youtube_url': 'Please provide a valid YouTube URL',
    'room_not_found': 'Room not found. Please check the room code.',
    'room_full': 'Room is full. Please try another room.',
    'invalid_username': 'Username must be 2-20 characters long.',
    'message_too_long': 'Message is too long. Maximum 500 characters.',
    'rate_limit_exceeded': 'You are sending messages too quickly. Please wait.',
    'video_not_available': 'This video is not available for embedding.',
    'network_error': 'Network error. Please check your connection.',
    'server_error': 'Server error. Please try again later.',
    'unauthorized': 'You are not authorized to perform this action.',
    'session_expired': 'Your session has expired. Please refresh the page.'
}

# Success Messages
SUCCESS_MESSAGES = {
    'room_created': 'Room created successfully!',
    'room_joined': 'Successfully joined the room!',
    'message_sent': 'Message sent successfully!',
    'playback_updated': 'Playback state updated!',
    'user_left': 'User left the room.',
    'settings_saved': 'Settings saved successfully!'
}

# Validation Patterns
VALIDATION_PATTERNS = {
    'youtube_url': r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
    'room_code': r'^[A-Z0-9]{8}$',
    'username': r'^[a-zA-Z0-9\s\-_]{2,20}$',
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
}

# Default Values
DEFAULT_VALUES = {
    'room_name': 'Untitled Room',
    'username': 'Anonymous',
    'video_quality': 'medium',
    'chat_enabled': True,
    'host_controls_enabled': True
}

# Cache Configuration
CACHE_TTL = {
    'video_info': 3600,      # 1 hour
    'room_data': 300,        # 5 minutes
    'user_data': 1800,       # 30 minutes
    'chat_messages': 60      # 1 minute
}

# Rate Limiting
RATE_LIMITS = {
    'chat_messages': 5,      # messages per minute
    'room_creation': 10,     # rooms per hour
    'room_joining': 30,      # joins per minute
    'api_requests': 100      # requests per minute
}

# Logging Configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': LOG_LEVEL,
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': LOG_LEVEL,
            'propagate': False
        }
    }
}

def get_config_value(key: str, default=None):
    """Get configuration value with fallback to default"""
    return globals().get(key, default)

def is_feature_enabled(feature: str) -> bool:
    """Check if a feature is enabled"""
    feature_flags = {
        'firebase': ENABLE_FIREBASE,
        'websocket': ENABLE_WEBSOCKET,
        'chat': ENABLE_CHAT,
        'user_presence': ENABLE_USER_PRESENCE,
        'host_controls': ENABLE_HOST_CONTROLS,
        'video_info': ENABLE_VIDEO_INFO
    }
    return feature_flags.get(feature, False)

def get_error_message(error_key: str) -> str:
    """Get error message by key"""
    return ERROR_MESSAGES.get(error_key, 'An unknown error occurred.')

def get_success_message(success_key: str) -> str:
    """Get success message by key"""
    return SUCCESS_MESSAGES.get(success_key, 'Operation completed successfully.')

def get_validation_pattern(pattern_key: str) -> str:
    """Get validation pattern by key"""
    return VALIDATION_PATTERNS.get(pattern_key, '')

def get_default_value(key: str):
    """Get default value by key"""
    return DEFAULT_VALUES.get(key)

def get_cache_ttl(cache_key: str) -> int:
    """Get cache TTL by key"""
    return CACHE_TTL.get(cache_key, 300)

def get_rate_limit(limit_key: str) -> int:
    """Get rate limit by key"""
    return RATE_LIMITS.get(limit_key, 10) 