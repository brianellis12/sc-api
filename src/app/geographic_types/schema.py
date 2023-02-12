from pydantic import BaseModel
from typing import Optional

class GeographicTypesBase(BaseModel):
    geoid: Optional[str]
    longitude: Optional[str]
    latitude: Optional[str]
    
class GeographicTypesCreate(GeographicTypesBase):
    pass