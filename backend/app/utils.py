import uuid
from datetime import datetime

def generate_room_code():
    return str(uuid.uuid4())[:8].upper()

def now_iso():
    return datetime.utcnow().isoformat() 