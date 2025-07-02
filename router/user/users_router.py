from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.conn import get_db
from model.response import APIResponse

from model.user.users import (
    UserCreate,
    UserDuplicateCheck,
    UserLogin,
    UserFind,
    UserResetPassword,
    UserSendOTP,
UserCheckOTP
)
from service.user import users_service

router = APIRouter()

@router.post("/createNewUser", response_model=APIResponse)
def createNewUser(user: UserCreate, db: Session = Depends(get_db)):
    return users_service.createNewUser(user, db)

@router.post("/checkDup", response_model=APIResponse)
def checkDup(user: UserDuplicateCheck, db: Session = Depends(get_db)):
    return users_service.checkDup(user, db)

@router.post("/login", response_model=APIResponse)
def userLogin(user: UserLogin, db: Session = Depends(get_db)):
    return users_service.userLogin(user, db)

#사용자 이메일로 사용자 ID 전송
@router.post("/findUser", response_model=APIResponse)
async def findUser(user: UserFind, db: Session = Depends(get_db)):
    return await users_service.findUser(user, db)

#사용자 이메일로 OTP 인증
@router.post("/sendOtp", response_model=APIResponse)
async def sendOtp(user: UserSendOTP, db: Session = Depends(get_db)):
    return await users_service.sendOtp(user, db)

# 사용자 OTP 인증 성공 시 이메일로 임시 비밀번호 송부
@router.post("/checkOtp", response_model=APIResponse)
async def checkOtp(user: UserCheckOTP, db: Session = Depends(get_db)):
    return await users_service.checkOtp(user, db)


@router.post("/resetPassword", response_model=APIResponse)
def resetPassword(user: UserResetPassword, db: Session = Depends(get_db)):
    return users_service.resetPassword(user, db)