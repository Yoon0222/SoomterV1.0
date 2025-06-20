from fastapi import APIRouter, Depends, UploadFile, File

from sqlalchemy.orm import Session

from model.map import Location, SearchByAddr

from database.conn import get_db
from model.response import APIResponse


from service import map_service

router = APIRouter()

@router.post("/saveLocation", response_model=APIResponse)
async def saveLocation(db: Session = Depends(get_db), file: UploadFile = File(...)):
    return await map_service.saveLocation(file, db)

@router.post("/getLocations", response_model=APIResponse)
def getLocations(loc : Location, db: Session = Depends(get_db)):
    return map_service.getLocations(loc, db)

@router.post("/searchNearby", response_model=APIResponse)
def searchNearby(loc : SearchByAddr, db: Session = Depends(get_db)):
    return map_service.getLocationsByName(loc, db)