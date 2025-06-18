from pydantic import BaseModel
from typing import Optional

class QueueItem(BaseModel):
    id: str
    room_code: str
    url: str
    added_by: str
    votes: int = 0
    added_at: str 