from pydantic import BaseModel
from typing import Optional

"""
Census Variables Schema
"""
class CensusVariablesBase(BaseModel):
    variable: Optional[str]
    label: Optional[str]
    section: Optional[str]
    group: Optional[str]

"""
Schema for adding Census Variables to the database   
"""
class CensusVariablesCreate(CensusVariablesBase):
    pass



