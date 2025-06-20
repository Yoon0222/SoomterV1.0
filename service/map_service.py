from passlib.context import CryptContext
from sqlalchemy.orm import Session
from model.code import fail, success

from fastapi import UploadFile, File
import csv, requests
from io import StringIO

from model.map import LocationTable, LocationOut

from utils.response import make_response

from math import pi, cos, sin, sqrt, atan2, radians

def get_latlng_from_naver(address: str):
    headers = {
        "X-NCP-APIGW-API-KEY-ID": "YOUR_CLIENT_ID",
        "X-NCP-APIGW-API-KEY": "YOUR_CLIENT_SECRET"
    }
    params = {"query": address}
    res = requests.get("https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode", headers=headers, params=params)

    if res.status_code == 200:
        items = res.json().get("addresses")
        if items:
            return float(items[0]["y"]), float(items[0]["x"])  # 위도, 경도
    return None

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
    csv_reader = csv.reader(StringIO(decoded), delimiter="\t")

    next(csv_reader, None)

    for row in csv_reader:
        place = row[0].split(',')
        location_model = LocationTable(
            AreaName=place[0],
            AreaType=place[1],
            Latitude=float(place[2]),
            Longitude=float(place[3]),
            AreaAddress=place[4]
        )
        db.add(location_model)
        db.commit()

    return make_response(code=success)


def getLocationsByName(loc, db):
    match = db.query(LocationTable).filter(LocationTable.AreaAddress.like(loc.LocationAddr)).first()

    if match:
        latitude, longitude = match.Latitude, match.Longitude
    else:
        # 2. NAVER API 호출
        coords = get_latlng_from_naver(loc.LocationAddr)
        if not coords:
            return make_response(code=fail, message="주소를 찾을 수 없습니다", error="Address Not Found")
        latitude, longitude = coords

    R = 6371
    delta_lat = (1.0 / R) * (180 / pi)
    delta_lng = delta_lat / cos(radians(latitude))

    min_lat = latitude - delta_lat
    max_lat = latitude + delta_lat
    min_lng = longitude - delta_lng
    max_lng = longitude + delta_lng

    candidates = db.query(LocationTable).filter(
        LocationTable.Latitude.between(min_lat, max_lat),
        LocationTable.Longitude.between(min_lng, max_lng)
    ).all()

    filtered = [
        area for area in candidates
        if haversine(latitude, longitude, area.Latitude, area.Longitude) <= 1.0
    ]

    return make_response(data=filtered, code=success, schema_class=LocationOut)