from fastapi import APIRouter
import database.integration as integration

router = APIRouter()

# Convert longitude and latitude to GEOID, then send it back to the client to hold the location's state
@router.get("/geoid")
async def get_geoid(longitude: str, latitude: str):
    return await integration.GeographicTypes.convert_coordinates(longitude, latitude)