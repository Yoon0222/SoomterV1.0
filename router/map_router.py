from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from model.map import Location

from model.response import APIResponse
from utils.response import make_response
from database.conn import get_db


from service import map_service

router = APIRouter()

@router.get("/getLocations")
def getLocations(loc : Location, db: Session = Depends(get_db)):
    return map_service.getLocations(loc, db)