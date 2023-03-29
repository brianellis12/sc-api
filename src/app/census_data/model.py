from sqlalchemy import Column, Text, Integer
from database.db import base

"""
Model for the Census Variables table
"""
class CensusVariables(base):

    __tablename__ = "census_variables"

    id = Column(Integer, primary_key=True)
    variable = Column(Text, nullable=True)
    label = Column(Text, nullable=True)
    section = Column(Text, nullable=True)
    group = Column(Text, nullable=True)
