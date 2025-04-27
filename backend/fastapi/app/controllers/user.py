from typing import Optional
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from ..services.user import UserService
from ..schemas.user import (
    AbstractUserResponse,
    UserResponse,
    UserCreateRequest,
    UserUpdateRequest,
    UserLoginRequest,
    UserResetPasswordRequest,
    UserForgotPasswordRequest,
    UsersReadRequest,
    UsersResponse,
)
from ..schemas.response import StandardResponse, ErrorResponse
from ..db.mongo import get_user_collection
from ..utils.password import generate_salt, hash_password, verify_password
from ..utils.smtp import SMTPMailService
from ..utils.otp import generate_otp, verify_otp, evict_otp
from ..utils.jwt import create_tokens, verify_tokens
from ..utils.file import upload_file, update_file, delete_file

router = APIRouter()


@router.post(
    "/signup",
    response_model=StandardResponse[UserResponse],
    responses={
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def signup(
    user: UserCreateRequest,
    service: UserService = Depends(get_user_collection),
):
    try:
        existing_user = await service._get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        salt = generate_salt()
        _, hashed_password = hash_password(user.password, salt)
        result = await service.create_user(
            email=user.email, name=user.name, salt=salt, hashed_password=hash_password
        )
        return StandardResponse(
            status=200,
            message="User has been created",
            data=result,
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


@router.post(
    "/login",
    response_model=StandardResponse[UserResponse],
    responses={
        401: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def login(
    user: UserLoginRequest,
    service: UserService = Depends(get_user_collection),
):
    try:
        existing_user = await service._get_user_by_email(user.email)
        if not existing_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not verify_password(
            user.password, existing_user.salt, existing_user.hashed_password
        ):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        tokens = await create_tokens(user_id=existing_user.id)
        return JSONResponse(
            status_code=500,
            headers={**tokens},
            content=StandardResponse(
                status=200,
                message="User has been logged in",
                data=existing_user,
            ),
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


@router.post(
    "/forgot-password",
    response_model=StandardResponse,
    responses={
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def forgot_password(
    request: UserForgotPasswordRequest,
    service: UserService = Depends(get_user_collection),
):
    try:
        existing_user = await service._get_user_by_email(request.email)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        mail_service = SMTPMailService()
        await mail_service.send_mail(
            to=[request.email],
            subject="Hello from TODO!",
            body=f"Your OTP for todo is {await generate_otp(request.email)}",
        )
        return StandardResponse(
            status=200, message="Forgot password otp has been sent to your mail"
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


@router.post(
    "/reset-password",
    response_model=StandardResponse,
    responses={
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def reset_password(
    request: UserResetPasswordRequest,
    service: UserService = Depends(get_user_collection),
):
    try:
        existing_user = await service._get_user_by_email(request.email)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        verified = await verify_otp(request.email, request.otp)
        salt = generate_salt()
        _, hashed_password = hash_password(request.password, salt)
        result = await service.reset_password(
            email=request.email,
            salt=salt,
            hashed_password=hashed_password,
        )
        if verified:
            await evict_otp(request.email)
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


@router.get(
    "/read/all",
    response_model=StandardResponse[UsersResponse],
    responses={
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def read_users(
    filter: UsersReadRequest, service: UserService = Depends(get_user_collection)
):
    try:
        users = service.list_users(filter=filter)
        return StandardResponse(
            status=200, message="Users have been read successfully", data=users
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
    "/read/{user_id}",
    response_model=StandardResponse[AbstractUserResponse],
    responses={
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def read_user(user_id: str, service: UserService = Depends(get_user_collection)):
    try:
        user = service.get_user(id=user_id)
        return StandardResponse(
            status=200, message="User have been read successfully", data=user
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


@router.put(
    "/update",
    response_model=StandardResponse[UserResponse],
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def update_user(
    user: UserUpdateRequest = Depends(),
    file: Optional[UploadFile] = File(None),
    service: UserService = Depends(get_user_collection),
    tokens: dict = Depends(verify_tokens),
):
    try:
        url = None
        if file:
            url = await upload_file(file_obj=file, bucket_name="user")
        result = service.update_user(user_id=tokens.get("user_id"), data=user, url=url)
        return StandardResponse(
            status=200, message="User have been read successfully", data=result
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
    "/delete",
    response_model=StandardResponse,
    responses={
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def delete_user(
    service: UserService = Depends(get_user_collection),
    tokens: dict = Depends(verify_tokens),
):
    try:
        result = await service.delete_user(user_id=tokens.get("user_id"))
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
