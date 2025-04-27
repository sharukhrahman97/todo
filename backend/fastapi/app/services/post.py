from typing import Optional
from fastapi import HTTPException
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.post import Post as PostModel
from ..schemas.post import CreatePostRequest, ReadPostsRequest, UpdatePostRequest
import uuid
from dataclasses import asdict


async def create_post(
    db: AsyncSession,
    post: CreatePostRequest,
    user_id: uuid.UUID,
    url: Optional[str] = None,
):
    db_item = PostModel(url=url, user_id=user_id, **asdict(post))
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def read_post(db: AsyncSession, post_id: uuid.UUID):
    result = await db.execute(
        select(PostModel).where(PostModel.id == post_id, PostModel.is_active == True)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


async def read_posts(db: AsyncSession, filter: ReadPostsRequest):
    query = (
        select(PostModel)
        .where(PostModel.is_active == True)
        .where(
            or_(
                PostModel.title.ilike(filter.q),
                PostModel.description.ilike(filter.q),
                PostModel.id == filter.q,
            )
        )
        .offset(filter.skip - 1 if filter.skip - 1 > 0 else 0)
        .limit(filter.limit)
    )
    result = await db.execute(query)
    posts = result.scalars().all()
    return posts


async def update_post(
    db: AsyncSession,
    post_id: uuid.UUID,
    post: UpdatePostRequest,
    url: Optional[str] = None,
):
    result = await db.execute(
        select(PostModel).where(PostModel.id == post_id, PostModel.is_active == True)
    )
    db_post = result.scalar_one_or_none()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    post_data = post.__dict__
    for key, value in post_data.items():
        setattr(db_post, key, value)

    if url is not None:
        db_post.url = url

    await db.commit()
    await db.refresh(db_post)
    return db_post


async def delete_post(db: AsyncSession, post_id: uuid.UUID):
    result = await db.execute(
        select(PostModel).where(PostModel.id == post_id, PostModel.is_active == True)
    )
    db_post = result.scalar_one_or_none()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    await db.delete(db_post)
    await db.commit()

    # Verify deletion
    result = await db.execute(select(PostModel).where(PostModel.id == post_id))
    verify_post = result.scalar_one_or_none()
    if verify_post:
        raise Exception(f"Post {post_id} still exists after delete attempt.")

    return {"message": f"Post {post_id} deleted successfully"}


async def soft_delete_post(
    db: AsyncSession,
    post_id: uuid.UUID,
):
    result = await db.execute(
        select(PostModel).where(PostModel.id == post_id, PostModel.is_active == True)
    )
    db_post = result.scalar_one_or_none()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    db_post.is_active = False

    await db.commit()
    await db.refresh(db_post)
    return {"message": f"Post {post_id} soft deleted successfully"}


async def undo_soft_delete_post(
    db: AsyncSession,
    post_id: uuid.UUID,
):
    result = await db.execute(
        select(PostModel).where(PostModel.id == post_id, PostModel.is_active == False)
    )
    db_post = result.scalar_one_or_none()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    db_post.is_active = True

    await db.commit()
    await db.refresh(db_post)
    return db_post


async def read_soft_deleted_post(db: AsyncSession, post_id: uuid.UUID):
    result = await db.execute(
        select(PostModel).where(PostModel.id == post_id, PostModel.is_active == False)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


async def read_soft_deleted_posts(db: AsyncSession, filter: ReadPostsRequest):
    query = (
        select(PostModel)
        .where(PostModel.is_active == False)
        .where(
            or_(
                PostModel.title.ilike(filter.q),
                PostModel.description.ilike(filter.q),
                PostModel.id == filter.q,
            )
        )
        .offset(filter.skip - 1 if filter.skip - 1 > 0 else 0)
        .limit(filter.limit)
    )
    result = await db.execute(query)
    posts = result.scalars().all()
    return posts
