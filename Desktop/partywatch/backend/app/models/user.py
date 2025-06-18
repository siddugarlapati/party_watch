from pydantic import BaseModel
from typing import Optional, List

class User(BaseModel):
    id: str
    username: str
    avatar_url: Optional[str] = None
    online: bool = True
    friends: List[str] = []
    last_seen: Optional[str] = None 