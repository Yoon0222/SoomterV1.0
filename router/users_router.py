from fastapi import APIRouter

from model.response import APIResponse
from utils.response import make_response

router = APIRouter()

@router.get("/test")
def test():
    return {"test": "test"}

@router.post("/aaUser", response_model=APIResponse)
def newUser(name: str, ):
    return make_response(code=400, error="Fail")

@router.post("/newUser", response_model=APIResponse)
def newUser(name: str, ):

    return make_response(code=400, error="Fail")