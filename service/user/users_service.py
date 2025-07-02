from smtplib import SMTPException

from utils.exception import CustomAPIException
from model.user.users import UserCreate, UsersTable
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from model.code import fail, success

from utils.response import make_response

from database.config import SMTP_HOST, SMTP_USER, SMTP_PASSWORD
from aiosmtplib import send
from email.message import EmailMessage
import random

# 전역에서 재사용 가능한 bcrypt 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def createNewUser(user: UserCreate, db: Session):
    existing_user = db.query(UsersTable).filter(
        UsersTable.UserId == user.UserId,
        UsersTable.UserEmail != user.UserEmail
    ).first()
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


async def findUser(user, db):

    existing_user = db.query(UsersTable).filter(UsersTable.UserEmail == user.UserEmail).first()
    if user:
        email = existing_user.UserEmail
        id = existing_user.UserId

        message = EmailMessage()
        message["from"] = SMTP_USER
        message["to"] = email
        message["subject"] = "숨터 ID"
        message.set_content(f"ID: {id} \n")
        try:
            await send(
                message,
                hostname=SMTP_HOST,
                port=465,
                username=SMTP_USER,
                password=SMTP_PASSWORD,
                use_tls=True,
                start_tls=False
            )
        except SMTPException:
            raise CustomAPIException(code=fail, message="SMTP Error")
        except Exception as e:
            raise CustomAPIException(code=fail, message=str(e))
    else:
        return make_response(error="User Not Found", code=fail)

    return make_response(code=success, message="email send success")


def resetPassword(user, db):

    hashed_password = pwd_context.hash(user.Password)
    quser = db.query(UsersTable).filter(UsersTable.UserId == user.UserId).first()
    if quser:
        quser.Password = hashed_password
        db.commit()
        db.refresh(quser)
        return make_response(code=success, message="Reset Password Success")

    return make_response(error="User Not Found", code=fail)


async def sendOtp(user, db):
    existing_user = db.query(UsersTable).filter(UsersTable.UserId == user.UserId).first()
    if existing_user:
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        existing_user.OTP = otp
        db.commit()
        db.refresh(existing_user)

        message = EmailMessage()
        message["from"] = SMTP_USER
        message["to"] = existing_user.UserEmail
        message["subject"] = "숨터 OTP 코드"
        message.set_content(f"OTP: {otp} \n")
        try:
            await send(
                message,
                hostname=SMTP_HOST,
                port=465,
                username=SMTP_USER,
                password=SMTP_PASSWORD,
                use_tls=True,
                start_tls=False
            )
        except SMTPException:
            raise CustomAPIException(code=fail, message="SMTP Error")
        except Exception as e:
            raise CustomAPIException(code=fail, message=str(e))

        return make_response(code=success, message="Send OTP Success")

    return make_response(error="User Not Found", code=fail)


async def checkOtp(user, db):
    existing_user = db.query(UsersTable).filter(
        UsersTable.UserId == user.UserId,
        UsersTable.OTP == user.OTP
    ).first()
    if existing_user:
        rand_pwd = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        hashed_password = pwd_context.hash(rand_pwd)
        existing_user.Password = hashed_password
        db.commit()
        db.refresh(existing_user)

        message = EmailMessage()
        message["from"] = SMTP_USER
        message["to"] = existing_user.UserEmail
        message["subject"] = "숨터 임시 비밀번호"
        message.set_content(f"임시 Password: {rand_pwd} \n")
        try:
            await send(
                message,
                hostname=SMTP_HOST,
                port=465,
                username=SMTP_USER,
                password=SMTP_PASSWORD,
                use_tls=True,
                start_tls=False
            )
        except SMTPException:
            raise CustomAPIException(code=fail, message="SMTP Error")
        except Exception as e:
            raise CustomAPIException(code=fail, message=str(e))

        return make_response(code=success, message="OTP Check Success")

    return make_response(error="OTP Not Found", code=fail)