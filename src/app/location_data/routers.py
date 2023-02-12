from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import db, integration

router = APIRouter()

@router.get("/")
async def root():
    return {"Hello": "World"}


@router.get("/location/age")
async def get_age_data(latitude: int, longitude: int): # remove db if not using db in integrations
    return {await integration.get_age_data(latitude, longitude)}