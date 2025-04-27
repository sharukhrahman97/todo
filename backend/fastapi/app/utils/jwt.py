import os
import uuid
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from dotenv import load_dotenv
from fastapi import Request, HTTPException, Header, Depends, Response

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_TIMEOUT = os.getenv("JWT_TIMEOUT", "15m")
REFRESH_TIMEOUT = os.getenv("REFRESH_TIMEOUT", "7d")
MODE = os.getenv("MODE", "0")


def _parse_expiration(duration_str: str) -> timedelta:
    if duration_str.endswith("m"):
        return timedelta(minutes=int(duration_str[:-1]))
    elif duration_str.endswith("h"):
        return timedelta(hours=int(duration_str[:-1]))
    elif duration_str.endswith("d"):
        return timedelta(days=int(duration_str[:-1]))
    return timedelta(minutes=15)


def _generate_unique_id() -> str:
    return uuid.uuid4().hex


async def create_tokens(user_id: str) -> dict:
    now = datetime.now(timezone.utc)
    access_token = jwt.encode(
        {
            "sub": user_id,
            "exp": now + _parse_expiration(JWT_TIMEOUT),
            "jti": _generate_unique_id(),
        },
        JWT_SECRET,
        algorithm="HS256",
    )
    refresh_token = jwt.encode(
        {
            "sub": user_id,
            "exp": now + _parse_expiration(REFRESH_TIMEOUT),
            "jti": _generate_unique_id(),
        },
        JWT_SECRET,
        algorithm="HS256",
    )
    return {"cl_x_token": access_token, "cl_x_refresh": refresh_token}


async def verify_tokens(
    cl_x_token: str = Header(default=None),
    cl_x_refresh: str = Header(default=None),
):
    if not cl_x_token or not cl_x_refresh:
        raise HTTPException(status_code=401, detail="Tokens are missing")

    try:
        decoded = jwt.decode(cl_x_token, JWT_SECRET, algorithms=["HS256"])
        return {
            "user_id": decoded["sub"],
            "cl_x_token": cl_x_token,
            "cl_x_refresh": cl_x_refresh,
        }
    except JWTError:
        try:
            decoded_refresh = jwt.decode(cl_x_refresh, JWT_SECRET, algorithms=["HS256"])
            new_access_token = jwt.encode(
                {
                    "sub": decoded_refresh["sub"],
                    "exp": datetime.now(timezone.utc) + _parse_expiration(JWT_TIMEOUT),
                    "jti": _generate_unique_id(),
                },
                JWT_SECRET,
                algorithm="HS256",
            )
            return {
                "user_id": decoded_refresh["sub"],
                "cl_x_token": new_access_token,
                "cl_x_refresh": cl_x_refresh,
            }
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid tokens")
