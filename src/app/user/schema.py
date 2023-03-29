from pydantic import BaseModel
from typing import Optional

"""
Base user schema
"""
class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: str

"""
Create user schema
"""
class UserCreate(UserBase):
    pass

"""
Full user schema
"""
class User(UserBase):
    id: int

    class Config:
        orm_mode = True