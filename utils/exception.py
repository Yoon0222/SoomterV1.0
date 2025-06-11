from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from model.response import APIResponse  # 공통 응답 모델

class CustomAPIException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message


# FastAPI 예외 핸들러 등록용 함수
def register_exception_handlers(app):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=APIResponse(success=False, code=exc.status_code, data=None, error=str(exc.detail)).dict()
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content=APIResponse(success=False, code=422, data=None, error="Validation Error").dict()
        )

    @app.exception_handler(CustomAPIException)
    async def custom_exception_handler(request: Request, exc: CustomAPIException):
        return JSONResponse(
            status_code=exc.code,
            content=APIResponse(success=False, code=exc.code, data=None, error=exc.message).dict()
        )