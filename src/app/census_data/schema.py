from pydantic import BaseModel
from typing import Optional
from enum import Enum

class CensusVariablesBase(BaseModel):
    variable: Optional[str]
    label: Optional[str]
    section: Optional[str]
    group: Optional[str]
    
class CensusVariablesCreate(CensusVariablesBase):
    pass

class CensusGroups(Enum):
    SEX_AGE = 'B01'
    RACE = 'B02'
    ANCESTRY_LATINO = 'B03'
    ANCESTRY_NONLATINO = 'B04'
    PLACEOFBIRTH_NONUS = 'B05'
    PLACEOFBIRTH_US = 'B06'
    GEOGRAPHIC_MOBILITY = 'B07'
    TRANSPORTATION = 'B08'
    CHILDREN_SENIORS = 'B09'
    GRANDPARENTS_GRANDCHILDREN = 'B10'
    HOUSEHOLD = 'B11'
    MARITAL_STATUS = 'B12'
    BIRTHS = 'B13'
    EDUCATION_ENROLLMENT = 'B14'
    EDUCATION_ATTAINMENT = 'B15'
    LANGUAGES = 'B16'
    INCOME = 'B17'
    DISABILITIES = 'B18'
    INCOME_BY_HOUSEHOLD = 'B19'
    INCOME_BY_SEX = 'B20'
    VETERAN_STATUS = 'B21'
    FOOD_STAMP_UTILIZATION = 'B22'
    EMPLOYMENT_STATUS = 'B23' 
    OCCUPATIONS = 'B24'
    HOUSING_STANDARD = 'B25'
    HOUSING_GROUP_QUARTERS = 'B26'
    HEALTH_INSURANCE = 'B27'
    HOUSEHOLD_TECHNOLOGY = 'B28'
    VOTING_AGE = 'B29'




