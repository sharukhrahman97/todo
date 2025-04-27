from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.types import ASGIApp
from ..schemas.response import ErrorResponse


class LimitUploadSize(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, max_upload_size: int) -> None:
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ):
        if request.method == "POST":
            if "content-length" not in request.headers:
                return JSONResponse(
                    status_code=500,
                    content=ErrorResponse(
                        status=411,
                        message="Length required for file",
                    ).model_dump(),
                )

            content_length = int(request.headers["content-length"])
            if content_length > self.max_upload_size:
                return JSONResponse(
                    status_code=500,
                    content=ErrorResponse(
                        status=413,
                        message="File size is too large",
                    ).model_dump(),
                )
        return await call_next(request)