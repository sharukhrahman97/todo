from datetime import datetime
from typing import Annotated, List, Optional
from fastapi import File, Form, UploadFile
from pydantic import BaseModel,Field
import uuid
from dataclasses import dataclass

@dataclass
class CreatePostRequest():
    title: str = Form(...)
    description: Optional[str] = Form(None)
    is_draft: Optional[bool] = Form(None)

@dataclass
class UpdatePostRequest():
    id: uuid.UUID
    title: str = Form(...)
    description: Optional[str] = Form(None)
    is_draft: Optional[bool] = Form(None)


class ReadPostsRequest(BaseModel):
    q: Optional[str] = None
    skip: int = 1
    limit: int = 10


class PostResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str]
    is_draft: bool
    url: Optional[str]
    created_at: datetime
    updated_at: datetime

class PostsResponse(BaseModel):
    __root__: List[PostResponse]