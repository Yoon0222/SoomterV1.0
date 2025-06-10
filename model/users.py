from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from database.conn import Base, ENGINE


class UserTable(Base):
    __tableName__ = 'USERS'
