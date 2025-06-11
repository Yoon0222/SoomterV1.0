from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from pydantic import BaseModel
from database.conn import Base, ENGINE


class UserSTable(Base):
    __tableName__ = 'USERS'
    idx = Column(Integer, primary_key=True, autoincrement=True) #Index값
    UserId = Column(String(100), nullable=False) # 사용자ID
    CreationDate = Column(TIMESTAMP, server_default=func.now()) #계정생성날짜
    UserName = Column(String(100), nullable=False) #사용자이름
    Email = Column(String(100), nullable=False) #사용자이메일

class Users(BaseModel):
    idx : int
    UserId : String
    CreationDate : String
    UserName : String
    Email : String