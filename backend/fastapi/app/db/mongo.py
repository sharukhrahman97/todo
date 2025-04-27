import motor.motor_asyncio
from ..core.config import settings
from motor.motor_asyncio import AsyncIOMotorCollection

MONGO_HOST = settings.MONGO_HOST
MONGO_PORT = settings.MONGO_PORT

MONGO_URL = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"

# Initialize the MongoDB client
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

# Databases
user_db = mongo_client["user"]

# Collections
async def get_user_collection() -> AsyncIOMotorCollection:
    return user_db.get_collection("user_collection")
