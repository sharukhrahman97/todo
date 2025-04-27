from typing import Optional
import uuid
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.post import (
    CreatePostRequest,
    PostsResponse,
    UpdatePostRequest,
    ReadPostsRequest,
    PostResponse,
)
from ..schemas.response import StandardResponse, ErrorResponse
from ..services import post as post_service
from ..utils.file import upload_file, update_file, delete_file
from ..db.postgres import get_db

router = APIRouter()


@router.post(
    "/create",
    response_model=StandardResponse[PostResponse],
    responses={
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def create_post(
    post: CreatePostRequest = Depends(),
    file: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
):
    try:
        url = None
        if file:
            url = await upload_file(file_obj=file, bucket_name="post")
        result = await post_service.create_post(
            db=db,
            post=post,
            user_id=uuid.UUID("24a8737e-f098-44d7-a7d3-71d19eb04eef"),
            url=url,
        )
        return StandardResponse(
            status=200, message="Post has been created", data=result.__dict__
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                status=500,
                message="Internal server error",
                error={"type": type(e).__name__, "detail": str(e)},
            ).model_dump(),
        )


@router.get(
    "/read/{post_id}",
    response_model=StandardResponse[PostResponse],
    responses={
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def read_post(post_id: str, db: AsyncSession = Depends(get_db)):
    try:
        result = await post_service.read_post(db=db, post_id=post_id)
        return StandardResponse(
            status=200, message="Post has been read", data=result.__dict__
        )
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=ErrorResponse(
                status=e.status_code,
                message="Error occurred",
                error={"type": type(e).__name__, "detail": str(e.detail)},
            ).model_dump(),
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                status=500,
                message="Internal server error",
                error={"type": type(e).__name__, "detail": str(e)},
            ).model_dump(),
        )


@router.get(
    "/read/all",
    response_model=StandardResponse[PostsResponse],
    responses={
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def read_posts(
    filter: ReadPostsRequest = Depends(), db: AsyncSession = Depends(get_db)
):
    try:
        results = await post_service.read_posts(db=db, filter=filter)
        return StandardResponse(
            status=200, message="Posts have been read", data=results
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                status=500,
                message="Internal server error",
                error={"type": type(e).__name__, "detail": str(e)},
            ).model_dump(),
        )


@router.put(
    "/update",
    response_model=StandardResponse[PostResponse],
    responses={
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def update_post(
    post: UpdatePostRequest = Depends(),
    file: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
):
    try:
        existing_post = await post_service.read_post(db=db, post_id=post.id)
        if not existing_post:
            raise HTTPException(status_code=404, detail="Post not found")
        if file:
            if existing_post.url:
                url = await update_file(
                    existing_filename=existing_post.url,
                    file_obj=file,
                    bucket_name="post",
                )
            else:
                url = await upload_file(file_obj=file, bucket_name="post")
        else:
            url = None
        result = await post_service.update_post(
            db=db, post_id=post.id, post=post, url=url
        )
        return StandardResponse(
            status=200, message="Post has been updated", data=result.__dict__
        )
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=ErrorResponse(
                status=e.status_code,
                message="Error occurred",
                error={"type": type(e).__name__, "detail": str(e.detail)},
            ).model_dump(),
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                status=500,
                message="Internal server error",
                error={"type": type(e).__name__, "detail": str(e)},
            ).model_dump(),
        )


@router.delete(
    "/delete/{post_id}",
    response_model=StandardResponse,
    responses={
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def delete_post(post_id: str, db: AsyncSession = Depends(get_db)):
    try:
        existing_post = await post_service.read_post(db=db, post_id=post_id)
        if not existing_post:
            raise HTTPException(status_code=404, detail="Post not found")
        if existing_post.url:
            await delete_file(filename=existing_post.url, bucket_name="post")
        result = await post_service.delete_post(db=db, post_id=post_id)
        return StandardResponse(status=200, message=result["message"])
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=ErrorResponse(
                status=e.status_code,
                message="Error occurred",
                error={"type": type(e).__name__, "detail": str(e.detail)},
            ).model_dump(),
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                status=500,
                message="Internal server error",
                error={"type": type(e).__name__, "detail": str(e)},
            ).model_dump(),
        )


@router.delete("/soft-delete/{post_id}", response_model=StandardResponse)
async def soft_delete_post(
    post_id: str,
    db: AsyncSession = Depends(get_db),
    responses={
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
):
    try:
        existing_post = await post_service.read_post(db=db, post_id=post_id)
        if not existing_post:
            raise HTTPException(status_code=404, detail="Post not found")
        result = await post_service.soft_delete_post(db=db, post_id=post_id)
        return StandardResponse(status=200, message=result["message"])
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=ErrorResponse(
                status=e.status_code,
                message="Error occurred",
                error={"type": type(e).__name__, "detail": str(e.detail)},
            ).model_dump(),
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                status=500,
                message="Internal server error",
                error={"type": type(e).__name__, "detail": str(e)},
            ).model_dump(),
        )


@router.put("/undo-soft-delete/{post_id}", response_model=StandardResponse)
async def undo_soft_delete_post(
    post_id: str,
    db: AsyncSession = Depends(get_db),
    responses={
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
):
    try:
        existing_post = await post_service.read_soft_deleted_post(
            db=db, post_id=post_id
        )
        if not existing_post:
            raise HTTPException(status_code=404, detail="Post not found")
        result = await post_service.undo_soft_delete_post(db=db, post_id=post_id)
        return StandardResponse(
            status=200, message="Post has been recovered", data=result.__dict__
        )
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=ErrorResponse(
                status=e.status_code,
                message="Error occurred",
                error={"type": type(e).__name__, "detail": str(e.detail)},
            ).model_dump(),
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                status=500,
                message="Internal server error",
                error={"type": type(e).__name__, "detail": str(e)},
            ).model_dump(),
        )


@router.get(
    "soft-deleted/read/all",
    response_model=StandardResponse[PostsResponse],
    responses={
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def read_soft_deleted_posts(
    filter: ReadPostsRequest = Depends(), db: AsyncSession = Depends(get_db)
):
    try:
        results = await post_service.read_soft_deleted_posts(db=db, filter=filter)
        return StandardResponse(
            status=200, message="Posts have been read", data=results
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                status=500,
                message="Internal server error",
                error={"type": type(e).__name__, "detail": str(e)},
            ).model_dump(),
        )
