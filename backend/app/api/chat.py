from fastapi import APIRouter, HTTPException, Body
from app.models.chat import ChatMessage
from app.db.mongo import mongo_db
from app.utils import now_iso
from typing import List

router = APIRouter()

@router.post("/", response_model=ChatMessage)
async def send_message(msg: ChatMessage = Body(...)):
    msg.timestamp = now_iso()
    await mongo_db.chat.insert_one(msg.dict())
    return msg

@router.get("/{room_code}", response_model=List[ChatMessage])
async def get_messages(room_code: str):
    msgs = await mongo_db.chat.find({"room_code": room_code}).to_list(100)
    return [ChatMessage(**m) for m in msgs]

@router.patch("/{msg_id}", response_model=ChatMessage)
async def edit_message(msg_id: str, update: dict = Body(...)):
    await mongo_db.chat.update_one({"id": msg_id}, {"$set": update})
    msg = await mongo_db.chat.find_one({"id": msg_id})
    return ChatMessage(**msg)

@router.delete("/{msg_id}")
async def delete_message(msg_id: str):
    await mongo_db.chat.delete_one({"id": msg_id})
    return {"success": True}

@router.post("/{msg_id}/pin")
async def pin_message(msg_id: str):
    await mongo_db.chat.update_one({"id": msg_id}, {"$set": {"pinned": True}})
    return {"success": True} 