from sqlalchemy import Column, Text, Integer
from database.db import base

class CensusVariables(base):

    __tablename__ = "census_variables"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=True)
    label = Column(Text, nullable=True)
    concept = Column(Text, nullable=True)
    group = Column(Text, nullable=True)
