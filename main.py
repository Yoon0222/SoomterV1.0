import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from router.users_router import router as user_router
from router.main_router import router as main_router
from router.map_router import router as map_router
from utils.exception import register_exception_handlers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (개발용)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST 등)
    allow_headers=["*"],  # 모든 헤더 허용
)

register_exception_handlers(app)

app.include_router(user_router, prefix="/user", tags=["Users"])
app.include_router(main_router, prefix="/main", tags=["Main"])
app.include_router(map_router, prefix="/map", tags=["Map"])

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Soomter API",
        version="1.0.0",
        description="Soomter API Documentation",
        routes=app.routes,
    )
    openapi_schema["servers"] = [
        {"url": "", "description": "로컬테스트"},
        {"url": "/api", "description": "Base path for all API requests"},

    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) #reload=conf().PROJ_RELOAD
