from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import db, integration

router = APIRouter()

@router.get("/")
async def root():
    return {"Hello": "World"}

@router.get("/location")
async def get_location_data(latitude: int, longitude: int, db: Session = Depends(db.get_db)): 
    return integration.get_location_data(db, latitude, longitude)