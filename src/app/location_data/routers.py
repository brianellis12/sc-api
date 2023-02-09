from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import db, integration

router = APIRouter()

@router.get("/")
async def root():
    return {"Hello": "World"}

@router.get("/location")
async def get_location_data(latitude: int, longitude: int): # remove db if not using db in integrations
    return {"goddamn": await integration.get_location_data(latitude, longitude)}