from sqlalchemy import Column, Integer, String, TIMESTAMP, Float
from sqlalchemy.sql import func
from pydantic import BaseModel
from database.conn import Base

class LocationTable(Base):
    __tablename__ = 'SMOKINGAREA'

    idx = Column(Integer, primary_key=True, autoincrement=True)         # 구역 ID
    AreaName = Column(String(100), nullable=False)
    Latitude = Column(Float, nullable=False)
    Longitude = Column(Float, nullable=False)
    CreationDate = Column(TIMESTAMP, nullable=False, server_default=func.now())

class Location(BaseModel):
    Latitude : float
    Longitude : float

