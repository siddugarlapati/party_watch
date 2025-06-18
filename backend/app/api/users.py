from fastapi import APIRouter, HTTPException, Body
from app.models.user import User
from app.db.mongo import mongo_db
from app.utils import now_iso
from typing import List

router = APIRouter()

@router.post("/", response_model=User)
async def create_user(user: User = Body(...)):
    user.last_seen = now_iso()
    await mongo_db.users.insert_one(user.dict())
    return user

@router.get("/", response_model=List[User])
async def list_users():
    users = await mongo_db.users.find({}).to_list(100)
    return [User(**u) for u in users]

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    user = await mongo_db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**user)

@router.patch("/{user_id}", response_model=User)
async def update_user(user_id: str, update: dict = Body(...)):
    await mongo_db.users.update_one({"id": user_id}, {"$set": update})
    user = await mongo_db.users.find_one({"id": user_id})
    return User(**user) 