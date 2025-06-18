from fastapi import APIRouter, HTTPException, status, Body
from app.models.room import Room
from app.db.mongo import mongo_db
from app.utils import generate_room_code, now_iso
from typing import List

router = APIRouter()

@router.post("/", response_model=Room)
async def create_room(room: Room = Body(...)):
    room.code = generate_room_code()
    room.created_at = now_iso()
    room.updated_at = now_iso()
    await mongo_db.rooms.insert_one(room.dict())
    return room

@router.get("/", response_model=List[Room])
async def list_rooms():
    rooms = await mongo_db.rooms.find({}).to_list(100)
    return [Room(**r) for r in rooms]

@router.get("/{code}", response_model=Room)
async def get_room(code: str):
    room = await mongo_db.rooms.find_one({"code": code})
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return Room(**room)

@router.post("/{code}/join")
async def join_room(code: str, user_id: str = Body(...), password: str = Body(None)):
    room = await mongo_db.rooms.find_one({"code": code})
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if not room.get("is_public", True):
        if not password or password != room.get("password"):
            raise HTTPException(status_code=403, detail="Incorrect password")
    if user_id not in room["users"]:
        room["users"].append(user_id)
        await mongo_db.rooms.update_one({"code": code}, {"$set": {"users": room["users"], "updated_at": now_iso()}})
    return {"success": True}

@router.patch("/{code}", response_model=Room)
async def update_room(code: str, update: dict = Body(...)):
    await mongo_db.rooms.update_one({"code": code}, {"$set": update})
    room = await mongo_db.rooms.find_one({"code": code})
    return Room(**room)

@router.delete("/{code}")
async def delete_room(code: str):
    await mongo_db.rooms.delete_one({"code": code})
    return {"success": True} 