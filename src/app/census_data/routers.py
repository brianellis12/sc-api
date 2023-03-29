from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import db, integration, crud
from app.authentication.routers import get_authenticated_user

router = APIRouter(dependencies=[Depends(get_authenticated_user)])

"""
Retrieve all of the sections for the inputted group
"""
@router.get("/location/sections")
def get_group_sections(group: str, db: Session = Depends(db.get_db)):
    return crud.CensusTypes.get_sections(db, group)

"""
Retrieve the statistics and labels for the inputted section and location
"""
@router.get("/location/data")
async def get_census_data(state: str, county: str, tract: str, section: str, db: Session = Depends(db.get_db)):
    return await integration.CensusTypes.get_census_data(db, state, county, tract, section)