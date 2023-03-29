from typing import Optional
from pydantic import BaseModel

from app.user.schema import User

"""
Authentication Request object
"""
class AuthenticateRequest(BaseModel):
    token: str
    first_name: Optional[str]
    last_name: Optional[str]

"""
Authentication Response object
"""
class AuthenticateResponse(BaseModel):
    incomplete_token: bool
    access_token: Optional[str]
    user: Optional[User]
    new_user: Optional[bool]
