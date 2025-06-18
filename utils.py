import re
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
import pytube
from urllib.parse import urlparse, parse_qs

class VideoUtils:
    """Utility class for video-related operations"""
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """Extract YouTube video ID from various URL formats"""
        if not url:
            return None
        
        # YouTube URL patterns
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'youtube\.com\/watch\?.*v=([^&\n?#]+)',
            r'youtube\.com\/v\/([^&\n?#]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    @staticmethod
    def get_video_info(video_id: str) -> Optional[Dict]:
        """Get video information using pytube"""
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            yt = pytube.YouTube(url)
            
            return {
                'title': yt.title,
                'author': yt.author,
                'length': yt.length,
                'views': yt.views,
                'description': yt.description,
                'thumbnail_url': yt.thumbnail_url,
                'publish_date': yt.publish_date.isoformat() if yt.publish_date else None
            }
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None
    
    @staticmethod
    def format_duration(seconds: int) -> str:
        """Format duration in seconds to HH:MM:SS or MM:SS"""
        if seconds < 3600:
            return f"{seconds // 60:02d}:{seconds % 60:02d}"
        else:
            return f"{seconds // 3600:02d}:{(seconds % 3600) // 60:02d}:{seconds % 60:02d}"
    
    @staticmethod
    def parse_timestamp(timestamp_str: str) -> Optional[int]:
        """Parse timestamp string (e.g., '1:30', '1:30:45') to seconds"""
        try:
            parts = timestamp_str.split(':')
            if len(parts) == 2:
                # MM:SS format
                return int(parts[0]) * 60 + int(parts[1])
            elif len(parts) == 3:
                # HH:MM:SS format
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            else:
                return None
        except ValueError:
            return None

class RoomUtils:
    """Utility class for room-related operations"""
    
    @staticmethod
    def generate_room_code() -> str:
        """Generate a unique 8-character room code"""
        return str(uuid.uuid4())[:8].upper()
    
    @staticmethod
    def validate_room_code(room_code: str) -> bool:
        """Validate room code format"""
        if not room_code:
            return False
        return len(room_code) == 8 and room_code.isalnum()
    
    @staticmethod
    def generate_user_id() -> str:
        """Generate a unique user ID"""
        return str(uuid.uuid4())
    
    @staticmethod
    def sanitize_username(username: str) -> str:
        """Sanitize username for display"""
        if not username:
            return "Anonymous"
        
        # Remove special characters and limit length
        sanitized = re.sub(r'[^\w\s-]', '', username.strip())
        return sanitized[:20] if sanitized else "Anonymous"
    
    @staticmethod
    def is_valid_username(username: str) -> bool:
        """Check if username is valid"""
        if not username or len(username.strip()) < 2:
            return False
        return len(username.strip()) <= 20

class ChatUtils:
    """Utility class for chat-related operations"""
    
    @staticmethod
    def sanitize_message(message: str) -> str:
        """Sanitize chat message"""
        if not message:
            return ""
        
        # Remove HTML tags and limit length
        sanitized = re.sub(r'<[^>]+>', '', message.strip())
        return sanitized[:500] if sanitized else ""
    
    @staticmethod
    def format_timestamp(timestamp: datetime) -> str:
        """Format timestamp for chat messages"""
        now = datetime.now()
        diff = now - timestamp
        
        if diff.days > 0:
            return timestamp.strftime("%b %d, %H:%M")
        elif diff.seconds > 3600:
            return timestamp.strftime("%H:%M")
        elif diff.seconds > 60:
            return f"{diff.seconds // 60}m ago"
        else:
            return "Just now"
    
    @staticmethod
    def detect_links(text: str) -> List[str]:
        """Detect URLs in text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, text)

class TimeUtils:
    """Utility class for time-related operations"""
    
    @staticmethod
    def get_current_timestamp() -> str:
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()
    
    @staticmethod
    def parse_iso_timestamp(timestamp_str: str) -> Optional[datetime]:
        """Parse ISO timestamp string"""
        try:
            return datetime.fromisoformat(timestamp_str)
        except ValueError:
            return None
    
    @staticmethod
    def is_recent(timestamp_str: str, minutes: int = 5) -> bool:
        """Check if timestamp is recent (within specified minutes)"""
        timestamp = TimeUtils.parse_iso_timestamp(timestamp_str)
        if not timestamp:
            return False
        
        return datetime.now() - timestamp < timedelta(minutes=minutes)
    
    @staticmethod
    def format_relative_time(timestamp_str: str) -> str:
        """Format timestamp as relative time"""
        timestamp = TimeUtils.parse_iso_timestamp(timestamp_str)
        if not timestamp:
            return "Unknown"
        
        now = datetime.now()
        diff = now - timestamp
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            return "Just now"

class SecurityUtils:
    """Utility class for security-related operations"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def generate_session_token() -> str:
        """Generate a secure session token"""
        return hashlib.sha256(f"{uuid.uuid4()}{datetime.now().isoformat()}".encode()).hexdigest()
    
    @staticmethod
    def validate_session_token(token: str) -> bool:
        """Validate session token format"""
        if not token:
            return False
        return len(token) == 64 and all(c in '0123456789abcdef' for c in token.lower())

class ValidationUtils:
    """Utility class for validation operations"""
    
    @staticmethod
    def is_valid_youtube_url(url: str) -> bool:
        """Check if URL is a valid YouTube URL"""
        if not url:
            return False
        
        # Check if it's a valid URL
        try:
            parsed = urlparse(url)
            if parsed.scheme not in ['http', 'https']:
                return False
        except:
            return False
        
        # Check if it's a YouTube domain
        youtube_domains = ['youtube.com', 'www.youtube.com', 'youtu.be', 'm.youtube.com']
        if parsed.netloc not in youtube_domains:
            return False
        
        # Check if it has a video ID
        return VideoUtils.extract_video_id(url) is not None
    
    @staticmethod
    def is_valid_room_name(name: str) -> bool:
        """Check if room name is valid"""
        if not name or len(name.strip()) < 3:
            return False
        return len(name.strip()) <= 50
    
    @staticmethod
    def is_valid_chat_message(message: str) -> bool:
        """Check if chat message is valid"""
        if not message or len(message.strip()) < 1:
            return False
        return len(message.strip()) <= 500

# Convenience functions
def extract_video_id(url: str) -> Optional[str]:
    """Extract YouTube video ID from URL"""
    return VideoUtils.extract_video_id(url)

def generate_room_code() -> str:
    """Generate unique room code"""
    return RoomUtils.generate_room_code()

def sanitize_username(username: str) -> str:
    """Sanitize username"""
    return RoomUtils.sanitize_username(username)

def format_duration(seconds: int) -> str:
    """Format duration to readable string"""
    return VideoUtils.format_duration(seconds)

def get_current_timestamp() -> str:
    """Get current timestamp"""
    return TimeUtils.get_current_timestamp()

def is_valid_youtube_url(url: str) -> bool:
    """Validate YouTube URL"""
    return ValidationUtils.is_valid_youtube_url(url) 