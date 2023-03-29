from fastapi import APIRouter, Depends
from app.authentication.routers import get_authenticated_user
import database.integration as integration

router = APIRouter(dependencies=[Depends(get_authenticated_user)])

"""
Convert longitude and latitude to GEOID, then send it back to the client to hold the location's state
"""
@router.get("/geoid")
async def get_geoid(longitude: str, latitude: str):
    return await integration.GeographicTypes.convert_coordinates(longitude, latitude)