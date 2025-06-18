from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, Text
from sqlalchemy.sql import func
from pydantic import BaseModel
from database.conn import Base


class ErrorLogTable(Base):
    __tablename__ = "ERROR_LOGS"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)
    error_message = Column(Text, nullable=False)
    traceback_detail = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    user_agent = Column(String(255))
    client_ip = Column(String(45))

