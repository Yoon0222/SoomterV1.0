from passlib.context import CryptContext
from sqlalchemy.orm import Session
from model.code import fail, success

from fastapi import UploadFile, File
import csv
from io import StringIO

from model.map import LocationTable, LocationOut

from utils.response import make_response

from math import pi, cos, sin, sqrt, atan2, radians

def haversine(lat1, lng1, lat2, lng2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))

def getLocations(loc, db):
    #전달받은 위도 경도를 통해 전방 1KM 지역에 있는 흡연구역 위도경도를 리턴

    R = 6371
    delta_lat = (1.0 / R) * (180 / pi)
    delta_lng = delta_lat / cos(radians(loc.Latitude))

    min_lat = loc.Latitude - delta_lat
    max_lat = loc.Latitude + delta_lat
    min_lng = loc.Longitude - delta_lng
    max_lng = loc.Longitude + delta_lng

    candidates = db.query(LocationTable).filter(
        LocationTable.Latitude.between(min_lat, max_lat),
        LocationTable.Longitude.between(min_lng, max_lng)
    ).all()

    filtered = [
        area for area in candidates
        if haversine(loc.Latitude, loc.Longitude, area.Latitude, area.Longitude) <= 1.0
    ]


    return make_response(data=filtered, code=success, schema_class=LocationOut)


async def saveLocation(file, db):
    if not file.filename.endswith(".csv"):
        return make_response(code=fail, message="csv 파일만 가능합니다.", error="fail")

    contents = await file.read()
    decoded = contents.decode("utf-8")
    csv_reader = csv.DictReader(StringIO(decoded))

    return None