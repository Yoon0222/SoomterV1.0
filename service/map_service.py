from passlib.context import CryptContext
from sqlalchemy.orm import Session
from model.code import fail, success

from model.map import LocationTable

from utils.response import make_response

from math import pi, cos, sin, sqrt, atan2, radians


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

    return make_response()