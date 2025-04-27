from dataclasses import dataclass
from datetime import datetime
import re
from fastapi import Form
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional
from bson import ObjectId
from ..utils.validator import PasswordStr


class UserModel(BaseModel):
    id: ObjectId = Field(alias="_id")
    email: EmailStr
    name: str
    avatar: Optional[str]
    description: Optional[str]
    salt: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime

    class Config:
        arbitrary_types_allowed = True


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    description: Optional[str]
    avatar: Optional[str]
    created_at: datetime
    updated_at: datetime


class AbstractUserResponse(BaseModel):
    email: EmailStr
    name: str
    description: Optional[str]
    avatar: Optional[str]
    created_at: datetime
    updated_at: datetime


class UserCreateRequest(BaseModel):
    email: EmailStr
    name: str
    password: PasswordStr


@dataclass
class UserUpdateRequest:
    name: Optional[str] = Form(None)
    description: Optional[str] = Form(None)


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: PasswordStr


class UserForgotPasswordRequest(BaseModel):
    email: EmailStr


class UserResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    password: PasswordStr


class UsersReadRequest(BaseModel):
    skip: int = (0,)
    limit: int = (10,)
    q: Optional[str] = (None,)


class UsersResponse(BaseModel):
    __root__: List[AbstractUserResponse]
