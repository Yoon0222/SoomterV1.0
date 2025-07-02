from model.user.users import UserLogin
from sqlalchemy.orm import Session

from utils.response import make_response
from model.code import success, fail

def adminLogin(admin: UserLogin, db: Session):
    is_admin = db.query(UserLogin).filter(
        UserLogin.UserId == admin.UserId,
        UserLogin.UserType == 1
    ).first()
    if not is_admin:
        return make_response(error="Not an Admin", code=fail)
    return make_response(code=success, message="Login Success")