from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from model.response import APIResponse
from utils.response import make_response
from model.users import UserCreate, UserDuplicateCheck, UserLogin
from database.conn import get_db


from service import users_service

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
