from pydantic import BaseModel
from typing import List, Optional

from app.aspect.schema import Aspect
from app.check_in.schema import CheckIn


class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: str
    practice_area: Optional[str]


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    is_admin: Optional[bool]

    class Config:
        orm_mode = True


class Profile(BaseModel):
    user: User
    active_hearts: List[Aspect]
    active_trees: List[Aspect]
    active_stars: List[Aspect]
    latest_checkin: Optional[CheckIn]
