from fastapi import APIRouter, HTTPException, Body
from app.db.mongo import mongo_db
from app.utils import now_iso
from typing import List
from pydantic import BaseModel

class Poll(BaseModel):
    id: str
    room_code: str
    question: str
    options: List[str]
    votes: dict
    created_at: str

router = APIRouter()

@router.post("/", response_model=Poll)
async def create_poll(poll: Poll = Body(...)):
    poll.created_at = now_iso()
    poll.votes = {opt: 0 for opt in poll.options}
    await mongo_db.polls.insert_one(poll.dict())
    return poll

@router.post("/{poll_id}/vote")
async def vote_poll(poll_id: str, option: str = Body(...)):
    poll = await mongo_db.polls.find_one({"id": poll_id})
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    if option not in poll["votes"]:
        raise HTTPException(status_code=400, detail="Invalid option")
    poll["votes"][option] += 1
    await mongo_db.polls.update_one({"id": poll_id}, {"$set": {"votes": poll["votes"]}})
    return {"success": True}

@router.get("/{room_code}", response_model=List[Poll])
async def get_polls(room_code: str):
    polls = await mongo_db.polls.find({"room_code": room_code}).to_list(20)
    return [Poll(**p) for p in polls] 