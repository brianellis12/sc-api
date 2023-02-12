from pydantic import BaseModel
from typing import Optional

class CensusVariablesBase(BaseModel):
    name: Optional[str]
    label: Optional[str]
    concept: Optional[str]
    group: Optional[str]
    
class CensusVariablesCreate(CensusVariablesBase):
    pass