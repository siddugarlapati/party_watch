from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
import uuid
from datetime import datetime

app = FastAPI(title="PartyWatch Backend")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data storage
rooms_db: Dict[str, Dict] = {}
chat_messages: Dict[str, List] = {}
private_chats: Dict[str, List] = {}  # Format: "user1_user2" -> messages
sprint_boards: Dict[str, Dict] = {}  # Format: room_code -> board data
meeting_notes: Dict[str, str] = {}   # Format: room_code -> notes

class RoomCreate(BaseModel):
    room_code: str
    host_id: str
    video_id: Optional[str] = None
    spotify_type: Optional[str] = None
    spotify_id: Optional[str] = None
    room_name: str
    room_type: str

class ChatMessage(BaseModel):
    room_code: str
    user_id: str
    username: str
    message: str

class PrivateMessage(BaseModel):
    sender_id: str
    receiver_id: str
    sender_username: str
    message: str

class JoinRoom(BaseModel):
    user_id: str
    username: Optional[str] = None
    password: Optional[str] = None

class SprintTask(BaseModel):
    room_code: str
    column: str  # "To Do", "In Progress", "Done"
    task: str
    user_id: str

class MeetingNotes(BaseModel):
    room_code: str
    notes: str
    user_id: str

@app.post("/api/rooms")
async def create_room(room_data: RoomCreate):
    """Create a new room"""
    room = {
        "room_code": room_data.room_code,
        "host_id": room_data.host_id,
        "video_id": room_data.video_id,
        "spotify_type": room_data.spotify_type,
        "spotify_id": room_data.spotify_id,
        "room_name": room_data.room_name,
        "room_type": room_data.room_type,
        "users": [room_data.host_id],
        "chat_messages": [],
        "created_at": datetime.now().isoformat(),
        "is_public": True,
        "password": None
    }
    rooms_db[room_data.room_code] = room
    chat_messages[room_data.room_code] = []
    private_chats[f"{room_data.room_code}_private"] = []
    sprint_boards[room_data.room_code] = {
        "To Do": [],
        "In Progress": [],
        "Done": []
    }
    meeting_notes[room_data.room_code] = ""
    return room

@app.get("/api/rooms/{room_code}")
async def get_room(room_code: str):
    """Get room information"""
    if room_code not in rooms_db:
        raise HTTPException(status_code=404, detail="Room not found")
    return rooms_db[room_code]

@app.post("/api/rooms/{room_code}/join")
async def join_room(room_code: str, join_data: JoinRoom):
    """Join an existing room"""
    if room_code not in rooms_db:
        raise HTTPException(status_code=404, detail="Room not found")
    
    room = rooms_db[room_code]
    if not room.get("is_public", True):
        if not join_data.password or join_data.password != room.get("password"):
            raise HTTPException(status_code=403, detail="Incorrect password")
    
    if join_data.user_id not in room["users"]:
        room["users"].append(join_data.user_id)
    
    return {
        "success": True,
        "spotify_type": room.get("spotify_type"),
        "spotify_id": room.get("spotify_id"),
        "room_desc": f"{room['room_type']} Room",
        "is_public": room.get("is_public", True),
        "password": room.get("password")
    }

@app.post("/api/chat/messages")
async def add_chat_message(message_data: ChatMessage):
    """Add a chat message"""
    if message_data.room_code not in rooms_db:
        raise HTTPException(status_code=404, detail="Room not found")
    
    message = {
        "id": str(uuid.uuid4()),
        "user_id": message_data.user_id,
        "username": message_data.username,
        "message": message_data.message,
        "timestamp": datetime.now().isoformat()
    }
    
    chat_messages[message_data.room_code].append(message)
    return message

@app.get("/api/chat/{room_code}/messages")
async def get_chat_messages(room_code: str):
    """Get chat messages for a room"""
    if room_code not in chat_messages:
        return []
    return chat_messages[room_code]

# Private Chat Endpoints
@app.post("/api/chat/private")
async def add_private_message(message_data: PrivateMessage):
    """Add a private message between two users"""
    chat_key = f"{min(message_data.sender_id, message_data.receiver_id)}_{max(message_data.sender_id, message_data.receiver_id)}"
    
    if chat_key not in private_chats:
        private_chats[chat_key] = []
    
    message = {
        "id": str(uuid.uuid4()),
        "sender_id": message_data.sender_id,
        "receiver_id": message_data.receiver_id,
        "sender_username": message_data.sender_username,
        "message": message_data.message,
        "timestamp": datetime.now().isoformat()
    }
    
    private_chats[chat_key].append(message)
    return message

@app.get("/api/chat/private/{user1_id}/{user2_id}")
async def get_private_messages(user1_id: str, user2_id: str):
    """Get private messages between two users"""
    chat_key = f"{min(user1_id, user2_id)}_{max(user1_id, user2_id)}"
    if chat_key not in private_chats:
        return []
    return private_chats[chat_key]

# Sprint Board Endpoints
@app.post("/api/sprint/task")
async def add_sprint_task(task_data: SprintTask):
    """Add a task to the sprint board"""
    if task_data.room_code not in sprint_boards:
        raise HTTPException(status_code=404, detail="Room not found")
    
    task = {
        "id": str(uuid.uuid4()),
        "task": task_data.task,
        "user_id": task_data.user_id,
        "created_at": datetime.now().isoformat()
    }
    
    sprint_boards[task_data.room_code][task_data.column].append(task)
    return task

@app.get("/api/sprint/{room_code}")
async def get_sprint_board(room_code: str):
    """Get sprint board for a room"""
    if room_code not in sprint_boards:
        return {"To Do": [], "In Progress": [], "Done": []}
    return sprint_boards[room_code]

@app.put("/api/sprint/{room_code}/move")
async def move_task(room_code: str, task_id: str, from_column: str, to_column: str):
    """Move a task between columns"""
    if room_code not in sprint_boards:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Find and move the task
    for column in sprint_boards[room_code].values():
        for task in column:
            if task["id"] == task_id:
                column.remove(task)
                sprint_boards[room_code][to_column].append(task)
                return {"success": True}
    
    raise HTTPException(status_code=404, detail="Task not found")

# Meeting Notes Endpoints
@app.post("/api/meeting/notes")
async def update_meeting_notes(notes_data: MeetingNotes):
    """Update meeting notes for a room"""
    if notes_data.room_code not in rooms_db:
        raise HTTPException(status_code=404, detail="Room not found")
    
    meeting_notes[notes_data.room_code] = notes_data.notes
    return {"success": True, "notes": notes_data.notes}

@app.get("/api/meeting/notes/{room_code}")
async def get_meeting_notes(room_code: str):
    """Get meeting notes for a room"""
    if room_code not in meeting_notes:
        return {"notes": ""}
    return {"notes": meeting_notes[room_code]}

# WebSocket endpoint for real-time features
@app.websocket("/ws/{room_code}")
async def websocket_endpoint(websocket: WebSocket, room_code: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "chat_message":
                # Broadcast chat message to all users in room
                await websocket.send_text(json.dumps({
                    "type": "chat_message",
                    "data": message.get("data")
                }))
            elif message.get("type") == "private_message":
                # Send private message to specific user
                await websocket.send_text(json.dumps({
                    "type": "private_message",
                    "data": message.get("data")
                }))
            elif message.get("type") == "sprint_update":
                # Broadcast sprint board update
                await websocket.send_text(json.dumps({
                    "type": "sprint_update",
                    "data": message.get("data")
                }))
            elif message.get("type") == "notes_update":
                # Broadcast meeting notes update
                await websocket.send_text(json.dumps({
                    "type": "notes_update",
                    "data": message.get("data")
                }))
            else:
                # Echo back for other messages
                await websocket.send_text(f"Echo: {data}")
    except Exception:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 