import firebase_admin
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv
import json
from datetime import datetime
from typing import Dict, List, Optional

load_dotenv()

class FirebaseManager:
    def __init__(self):
        self.db = None
        self.initialized = False
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase connection"""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                # Try to load from environment variable
                firebase_config = os.getenv('FIREBASE_CONFIG')
                if firebase_config:
                    cred_dict = json.loads(firebase_config)
                    cred = credentials.Certificate(cred_dict)
                else:
                    # Try to load from service account file
                    service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH')
                    if service_account_path and os.path.exists(service_account_path):
                        cred = credentials.Certificate(service_account_path)
                    else:
                        # Use default credentials (for local development)
                        cred = credentials.ApplicationDefault()
                
                # Initialize Firebase
                database_url = os.getenv('FIREBASE_DATABASE_URL', 'https://demo-project-default-rtdb.firebaseio.com/')
                firebase_admin.initialize_app(cred, {
                    'databaseURL': database_url
                })
            
            self.db = db.reference()
            self.initialized = True
            print("Firebase initialized successfully")
            
        except Exception as e:
            print(f"Firebase initialization failed: {e}")
            self.initialized = False
    
    def create_room(self, room_code: str, host_id: str, video_id: str = None, room_name: str = "Untitled Room") -> bool:
        """Create a new watch room"""
        if not self.initialized:
            return False
        
        try:
            room_data = {
                'host_id': host_id,
                'video_id': video_id,
                'room_name': room_name,
                'users': [host_id],
                'playback_state': {
                    'playing': False,
                    'current_time': 0,
                    'last_updated': datetime.now().isoformat()
                },
                'chat_messages': [],
                'created_at': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat()
            }
            
            self.db.child('rooms').child(room_code).set(room_data)
            return True
            
        except Exception as e:
            print(f"Error creating room: {e}")
            return False
    
    def join_room(self, room_code: str, user_id: str, username: str) -> bool:
        """Join an existing room"""
        if not self.initialized:
            return False
        
        try:
            room_ref = self.db.child('rooms').child(room_code)
            room_data = room_ref.get()
            
            if not room_data:
                return False
            
            # Add user to room
            users = room_data.get('users', [])
            if user_id not in users:
                users.append(user_id)
                room_ref.child('users').set(users)
            
            # Add user info
            user_info = {
                'id': user_id,
                'username': username,
                'joined_at': datetime.now().isoformat(),
                'is_host': user_id == room_data.get('host_id')
            }
            
            room_ref.child('user_info').child(user_id).set(user_info)
            room_ref.child('last_activity').set(datetime.now().isoformat())
            
            return True
            
        except Exception as e:
            print(f"Error joining room: {e}")
            return False
    
    def leave_room(self, room_code: str, user_id: str) -> bool:
        """Leave a room"""
        if not self.initialized:
            return False
        
        try:
            room_ref = self.db.child('rooms').child(room_code)
            room_data = room_ref.get()
            
            if not room_data:
                return False
            
            # Remove user from room
            users = room_data.get('users', [])
            if user_id in users:
                users.remove(user_id)
                room_ref.child('users').set(users)
            
            # Remove user info
            room_ref.child('user_info').child(user_id).delete()
            
            # If room is empty, delete it
            if not users:
                room_ref.delete()
            else:
                room_ref.child('last_activity').set(datetime.now().isoformat())
            
            return True
            
        except Exception as e:
            print(f"Error leaving room: {e}")
            return False
    
    def get_room(self, room_code: str) -> Optional[Dict]:
        """Get room data"""
        if not self.initialized:
            return None
        
        try:
            return self.db.child('rooms').child(room_code).get()
        except Exception as e:
            print(f"Error getting room: {e}")
            return None
    
    def update_playback_state(self, room_code: str, playback_state: Dict) -> bool:
        """Update playback state for a room"""
        if not self.initialized:
            return False
        
        try:
            playback_state['last_updated'] = datetime.now().isoformat()
            self.db.child('rooms').child(room_code).child('playback_state').set(playback_state)
            return True
        except Exception as e:
            print(f"Error updating playback state: {e}")
            return False
    
    def add_chat_message(self, room_code: str, user_id: str, username: str, message: str) -> bool:
        """Add a chat message to a room"""
        if not self.initialized:
            return False
        
        try:
            chat_message = {
                'id': f"msg_{datetime.now().timestamp()}",
                'user_id': user_id,
                'username': username,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
            
            # Add message to chat
            self.db.child('rooms').child(room_code).child('chat_messages').push(chat_message)
            
            # Update last activity
            self.db.child('rooms').child(room_code).child('last_activity').set(datetime.now().isoformat())
            
            return True
            
        except Exception as e:
            print(f"Error adding chat message: {e}")
            return False
    
    def get_room_users(self, room_code: str) -> List[Dict]:
        """Get all users in a room"""
        if not self.initialized:
            return []
        
        try:
            room_data = self.db.child('rooms').child(room_code).get()
            if not room_data:
                return []
            
            user_info = room_data.get('user_info', {})
            return list(user_info.values())
            
        except Exception as e:
            print(f"Error getting room users: {e}")
            return []
    
    def cleanup_inactive_rooms(self, max_inactive_hours: int = 24) -> int:
        """Clean up rooms that have been inactive for too long"""
        if not self.initialized:
            return 0
        
        try:
            from datetime import timedelta
            cutoff_time = datetime.now() - timedelta(hours=max_inactive_hours)
            
            rooms = self.db.child('rooms').get()
            if not rooms:
                return 0
            
            cleaned_count = 0
            for room_code, room_data in rooms.items():
                last_activity = room_data.get('last_activity')
                if last_activity:
                    last_activity_dt = datetime.fromisoformat(last_activity)
                    if last_activity_dt < cutoff_time:
                        self.db.child('rooms').child(room_code).delete()
                        cleaned_count += 1
            
            return cleaned_count
            
        except Exception as e:
            print(f"Error cleaning up rooms: {e}")
            return 0

# Global Firebase manager instance
firebase_manager = FirebaseManager()

# Helper functions for easy access
def create_room(room_code: str, host_id: str, video_id: str = None, room_name: str = "Untitled Room") -> bool:
    return firebase_manager.create_room(room_code, host_id, video_id, room_name)

def join_room(room_code: str, user_id: str, username: str) -> bool:
    return firebase_manager.join_room(room_code, user_id, username)

def leave_room(room_code: str, user_id: str) -> bool:
    return firebase_manager.leave_room(room_code, user_id)

def get_room(room_code: str) -> Optional[Dict]:
    return firebase_manager.get_room(room_code)

def update_playback_state(room_code: str, playback_state: Dict) -> bool:
    return firebase_manager.update_playback_state(room_code, playback_state)

def add_chat_message(room_code: str, user_id: str, username: str, message: str) -> bool:
    return firebase_manager.add_chat_message(room_code, user_id, username, message)

def get_room_users(room_code: str) -> List[Dict]:
    return firebase_manager.get_room_users(room_code) 