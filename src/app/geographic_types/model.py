from sqlalchemy import Column, Integer, Text
from database.db import base

class GeographicTypes(base):

    __tablename__ = "geographic_types"

    id = Column(Integer, primary_key=True)
    geoid = Column(Text, nullable=True)
    longitude = Column(Text, nullable=True)
    latitude = Column(Text, nullable=True)
