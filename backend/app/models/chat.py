from pydantic import BaseModel
from typing import Optional

class ChatMessage(BaseModel):
    id: str
    room_code: str
    user_id: str
    username: str
    message: str
    timestamp: str
    edited: Optional[bool] = False
    pinned: Optional[bool] = False 