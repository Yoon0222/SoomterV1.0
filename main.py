from dataclasses import asdict

import uvicorn
from fastapi import FastAPI
from common.config import conf
from database.conn import db


def create_app():

    c = conf()
    app = FastAPI()

    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)
    # 데이터 베이스 이니셜라이즈
    # 레디스 이니셜라이즈
    # 미들웨어 정의
    # 라우터 정의

    return app

app = FastAPI()
# app.include_router()
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True) #reload=conf().PROJ_RELOAD
