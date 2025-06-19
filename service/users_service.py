from utils.exception import CustomAPIException
from model.users import UserCreate, UsersTable
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from model.code import fail, success

from utils.response import make_response

# 전역에서 재사용 가능한 bcrypt 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ─────────────────────────────────────────────────────────────
# 🧩 회원가입
# ─────────────────────────────────────────────────────────────
def createNewUser(user: UserCreate, db: Session):
    existing_user = db.query(UsersTable).filter(UsersTable.UserId == user.UserId).first()
    if existing_user:
        return make_response(error=user.UserId+" already existing ID",code=fail)

    hashed_password = pwd_context.hash(user.Password)

    user_model = UsersTable(
        UserId=user.UserId,
        Password=hashed_password,
        UserEmail=user.UserEmail,
        UserName=user.UserName,
        UserPhone=user.UserPhone
    )

    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    return make_response(code=success, message="User Create Success")


def checkDup(user, db):
    existing_user = db.query(UsersTable).filter(UsersTable.UserId == user.UserId).first()
    if existing_user:
        return make_response(error=user.UserId + " already existing ID", code=fail)
    return make_response(code=success)


def userLogin(userlogin, db):
    user = db.query(UsersTable).filter(UsersTable.UserId == userlogin.UserId).first()

    if not user:
        return make_response(error="User Not Found", code=fail)
    if not pwd_context.verify(userlogin.Password,user.Password):
        return make_response(error="Incorrect password", code=fail)

    return make_response(code=success, message="Login Success")