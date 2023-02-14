from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import db, integration, crud

router = APIRouter()

@router.get("/")
async def root():
    return {"Hello": "World"}

@router.get("/location/sections")
def get_group_sections(group: str, db: Session = Depends(db.get_db)):
    return crud.CensusTypes.get_sections(db, group)

@router.get("/location/data")
async def get_census_data(state: str, county: str, tract: str, section: str, db: Session = Depends(db.get_db)):
    return await integration.CensusTypes.get_census_data(db, state, county, tract, section)