import logging
from fastapi import APIRouter, Depends
from app.authentication.routers import get_authenticated_user
import database.integration as integration

router = APIRouter(dependencies=[Depends(get_authenticated_user)])

"""
Convert longitude and latitude to GEOID, then send it back to the client to hold the location's state
"""
@router.get("/geoid")
async def get_geoid(longitude: str, latitude: str):
    logging.info(f"Entering get_geoid")
    logging.info(f"Converting coordinates {longitude}, {latitude} to GEOID")
    result = await integration.GeographicTypes.convert_coordinates(longitude, latitude)
    logging.info(f"Got result {result}")
    logging.info(f"Exiting get_geoid")
    return result