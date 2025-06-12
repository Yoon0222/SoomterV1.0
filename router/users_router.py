from fastapi import APIRouter

from model.response import APIResponse
from utils.response import make_response

router = APIRouter()

@router.get("/test")
def test():
    return {"test": "test"}

@router.post("/aaUser", response_model=APIResponse)
def aaUser(name: str, ):
    return make_response(code=400, error="Fail")

@router.post("/bbUser", response_model=APIResponse)
def bbUser(name: str, ):
    return make_response(code=400, error="Fail")
@router.post("/ccUser", response_model=APIResponse)
def ccUser(name: str, ):
    return make_response(code=400, error="Fail")

@router.post("/ddUser", response_model=APIResponse)
def ddUser(name: str, ):
    return make_response(code=400, error="Fail")


@router.post("/newUser", response_model=APIResponse)
def newUser(name: str, ):

    return make_response(code=400, error="Fail")