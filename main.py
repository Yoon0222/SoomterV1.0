import uvicorn
from fastapi import FastAPI
from router.users_router import router as user_router
from router.main_router import router as main_router
from utils.exception import register_exception_handlers

app = FastAPI()

register_exception_handlers(app)

app.include_router(user_router, prefix="/user", tags=["Users"])
app.include_router(main_router, prefix="/main", tags=["Main"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) #reload=conf().PROJ_RELOAD
