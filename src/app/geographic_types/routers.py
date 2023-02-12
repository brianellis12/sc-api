from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import db, crud

router = APIRouter()

# Convert longitude and latitude to GEOID, then send it back to the client to hold the location's state
@router.get("/geoid")
async def get_geoid(longitude: float, latitude: float, db: Session = Depends(db.get_db)):
    return {crud.geographic_types.get(db, longitude, latitude)}