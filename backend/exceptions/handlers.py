from fastapi.responses import JSONResponse
from fastapi import Request
from exceptions.base import AppException


async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "data": None,
            "error": {
                "message": exc.message,
                "code": exc.code,
            },
        },
    )
