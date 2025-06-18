from pydantic import BaseModel, Field
from typing import List, Optional

class Room(BaseModel):
    code: str
    host_id: str
    type: str = "YouTube"  # or Spotify, Screenshare
    description: Optional[str] = None
    password: Optional[str] = None
    is_public: bool = True
    users: List[str] = []
    created_at: str
    updated_at: str 