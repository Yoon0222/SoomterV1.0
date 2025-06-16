from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from database.config import DB_NAME, DB_PORT, DB_USER, DB_HOST, DB_PASSWORD

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
# DATABASE_URL = f"mysql+mysqlconnector://root:dbstlr23@172.31.37.150:3306/soomter?charset=utf8mb4"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# FastAPI 의존성 주입용
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()