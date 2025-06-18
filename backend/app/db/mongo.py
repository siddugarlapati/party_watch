import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "partywatch")

client = None
mongo_db = None

async def connect_to_mongo():
    global client, mongo_db
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    mongo_db = client[MONGO_DB]

async def close_mongo():
    global client
    if client:
        client.close() 