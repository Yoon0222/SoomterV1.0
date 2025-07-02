from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.conn import get_db
from model.response import APIResponse

from model.user.users import UserLogin
from service.admin import admin_service

router = APIRouter()

@router.post("/admin/adminLogin", response_model=APIResponse)
def adminLogin(admin: UserLogin, db: Session = Depends(get_db)):
    return admin_service.adminLogin(admin, db)

@router.get("/admin/genQr", response_model=APIResponse)
def genQr(db: Session = Depends(get_db)):
    return admin_service.genQR(db)