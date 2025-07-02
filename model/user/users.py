from sqlalchemy import Column, Integer, String, TIMESTAMP, UniqueConstraint
from sqlalchemy.sql import func
from pydantic import BaseModel
from database.conn import Base



class UsersTable(Base):
    __tablename__ = 'USERS'

    idx = Column(Integer, primary_key=True, autoincrement=True)         # 사용자 고유 ID
    UserId = Column(String(100), nullable=False)                        # 사용자 ID
    UserName = Column(String(100), nullable=False)                      # 사용자 이름
    UserEmail = Column(String(100), nullable=False)                         # 이메일
    Password = Column(String(200), nullable=False)                      # 암호화된 비밀번호
    CreationDate = Column(TIMESTAMP, server_default=func.now())        # 생성일시 (자동)
    UserPhone = Column(String(100), nullable=False)
    OTP = Column(String(10))
    UserType = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('UserEmail', name='user_email_unique'),
    )


class UserCreate(BaseModel):
    UserId : str
    Password : str
    UserEmail : str
    UserName : str
    UserPhone : str

class UserDuplicateCheck(BaseModel):
    UserId : str

class UserLogin(BaseModel):
    UserId : str
    Password : str

class UserFind(BaseModel):
    UserEmail : str

class UserSendOTP(BaseModel):
    UserId : str

class UserCheckOTP(BaseModel):
    UserId : str
    OTP : str

class UserResetPassword(BaseModel):
    UserId: str
    Password: str