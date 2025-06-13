from utils.exception import CustomAPIException
from model.users import UserCreate, UsersTable
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from utils.response import make_response

# 전역에서 재사용 가능한 bcrypt 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ─────────────────────────────────────────────────────────────
# 🧩 회원가입
# ─────────────────────────────────────────────────────────────
def createNewUser(user: UserCreate, db: Session):
    existing_user = db.query(UsersTable).filter(UsersTable.UserId == user.UserId).first()
    if existing_user:
        return make_response(data=user.UserId,error=user.UserId+" already existing ID",code=200)

    hashed_password = pwd_context.hash(user.Password)

    user_model = UsersTable(
        UserId=user.UserId,
        Password=hashed_password,
        Email="temp@test.com",
        UserName="테스트"
    )

    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    return make_response(data=user, code=200, message="성공")