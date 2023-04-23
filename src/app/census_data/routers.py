from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import db, integration, crud
from app.authentication.routers import get_authenticated_user
import logging
router = APIRouter(dependencies=[Depends(get_authenticated_user)])

"""
Retrieve all of the sections for the inputted group
"""
@router.get("/location/sections")
def get_group_sections(group: str, db: Session = Depends(db.get_db)):
    logging.info(f"Entering get_group_sections")
    logging.info(f"Getting sections for group {group}")
    result = crud.CensusTypes.get_sections(db, group)
    logging.info(f"Got {len(result)} sections")
    logging.info(f"Exiting get_group_sections")
    return result

"""
Retrieve the statistics and labels for the inputted section and location
"""
@router.get("/location/data")
async def get_census_data(state: str, county: str, tract: str, section: str, db: Session = Depends(db.get_db)):
    logging.info(f"Entering get_census_data")
    logging.info(f"Getting census data for state {state}, county {county}, tract {tract}, section {section}")
    result = await integration.CensusTypes.get_census_data(db, state, county, tract, section)
    logging.info(f"Got {len(result)} data points")
    logging.info(f"Exiting get_census_data")
    return result