from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from model.response import APIResponse  # 공통 응답 모델
from model.code import success, fail, req_validation_error, internal_error
from sqlalchemy.orm import Session
from database.conn import get_db  # 네가 쓰는 방식에 따라 조정
from model.error import ErrorLogTable  # 예: 로그 테이블

import traceback
import datetime

class CustomAPIException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message


# FastAPI 예외 핸들러 등록용 함수
def register_exception_handlers(app):
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        db: Session = next(get_db())

        db.add(ErrorLogTable(
            path=str(request.url),
            method=request.method,
            error_message=str(exc),
            traceback_detail=traceback.format_exc(),
            created_at=datetime.datetime.utcnow()
        ))
        db.commit()

        return JSONResponse(
            status_code=500,
            content=APIResponse(success=False, code=internal_error, error=str(exc)).dict()
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=APIResponse(success=False, code=fail, error=str(exc.detail)).dict()
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content=APIResponse(success=False, code=req_validation_error, error="Validation Error").dict()
        )

    @app.exception_handler(CustomAPIException)
    async def custom_exception_handler(request: Request, exc: CustomAPIException):
        return JSONResponse(
            status_code=500,
            content=APIResponse(success=False, code=fail, error=exc.message).dict()
        )