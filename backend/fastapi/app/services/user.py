from datetime import datetime, timezone
import re
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from fastapi import HTTPException, status
from pymongo import DESCENDING
from ..schemas.user import (
    AbstractUserResponse,
    UserModel,
    UserResponse,
    UserUpdateRequest,
    UsersReadRequest,
)


class UserService:
    def __init__(self, user_collection: AsyncIOMotorCollection):
        self.user_collection = user_collection

    async def _get_user_by_email(self, email: str):
        existing_user = await self.user_collection.find_one({"email": email})
        if existing_user is None:
            return None
        return UserResponse(
            id=str(existing_user["_id"]),
            email=existing_user["email"],
            name=existing_user["name"],
            description=existing_user.get("description"),
            avatar=existing_user.get("avatar"),
            created_at=existing_user["created_at"],
            updated_at=existing_user["updated_at"],
        )

    async def create_user(self, email: str, name: str, salt: str, hashed_password: str):
        now = datetime.now(timezone.utc)
        user = {
            "email": email,
            "name": name,
            "salt": salt,
            "hashed_password": hashed_password,
            "created_at": now,
            "updated_at": now,
        }
        result = await self.user_collection.insert_one(user)
        return UserResponse(
            id=str(result.inserted_id),
            email=user["email"],
            name=user["name"],
            description=None,
            avatar=None,
            created_at=user["created_at"],
            updated_at=user["updated_at"],
        )

    async def reset_password(self, email: str, salt: str, hashed_password: str):
        await self.user_collection.find_one_and_update(
            {"email": email},
            {
                "salt": salt,
                "hashed_password": hashed_password,
                "updated_at": datetime.now(timezone.utc),
            },
        )
        return {"message": "Password has been resetted successfully"}

    async def get_user(self, id: str) -> AbstractUserResponse:
        try:
            object_id = ObjectId(id)
        except Exception:
            raise HTTPException(status_code=422, detail="Invalid user ID format")

        existing_user = await self.user_collection.find_one({"_id": object_id})
        if not existing_user:
            raise HTTPException(status_code=404, detail="User doesn't exist")

        return AbstractUserResponse(
            email=existing_user["email"],
            name=existing_user["name"],
            description=existing_user.get("description"),
            avatar=existing_user.get("avatar"),
            created_at=existing_user["created_at"],
            updated_at=existing_user["updated_at"],
        )

    async def list_users(self, filter: UsersReadRequest) -> List[AbstractUserResponse]:
        query = {}

        if filter.q:
            regex = {
                "$regex": re.escape(filter.q),
                "$options": "i",
            }
            query = {
                "$or": [
                    {"email": regex},
                    {"name": regex},
                    {"description": regex},
                ]
            }
            try:
                object_id = ObjectId(filter.q)
                query["$or"].append({"_id": object_id})
            except Exception:
                pass

        users_cursor = (
            self.user_collection.find(query)
            .sort("created_at", DESCENDING)
            .skip(filter.skip)
            .limit(filter.limit)
        )

        users = []
        async for user in users_cursor:
            users.append(
                AbstractUserResponse(
                    email=user["email"],
                    name=user["name"],
                    description=user.get("description"),
                    avatar=user.get("avatar"),
                    created_at=user["created_at"],
                    updated_at=user["updated_at"],
                )
            )

        return users

    async def update_user(
        self, user_id: str, data: UserUpdateRequest, url: Optional[str] = None
    ):
        user = await self.user_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        updates = {}
        post_data = data.__dict__

        for key, value in post_data.items():
            updates[key] = value

        if url is not None:
            updates["avatar"] = url

        if not updates:
            raise HTTPException(status_code=400, detail="No valid fields to update")

        await self.user_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": updates}
        )

        user = await self.user_collection.find_one({"_id": ObjectId(user_id)})
        return UserResponse(
            id=str(user["_id"]),
            email=user["email"],
            name=user["name"],
            description=user.get("description"),
            avatar=user.get("avatar"),
            created_at=user["created_at"],
            updated_at=user["updated_at"],
        )

    async def delete_user(self, user_id):
        result = await self.user_collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User has been deleted successfully"}