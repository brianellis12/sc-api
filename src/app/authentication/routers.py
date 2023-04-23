from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
import logging

from app.config import Settings, get_settings
from app.user import model
from .schema import AuthenticateRequest
from database import authentication, db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

"""
Get user to validate authentication
"""
async def get_authenticated_user(token=Depends(oauth2_scheme)):
    logging.info(f"Entering get_authenticated_user")
    try:
        user = jwt.decode(token, key="myKey", algorithms=["HS256"])
        logging.info(f"Got user {user}")
        return user
    except jwt.DecodeError:
        logging.error(f"Invalid token")
        raise HTTPException(403, "Invalid token")
    logging.info(f"Exiting get_authenticated_user")

"""
Authenticate user logged in in the front end
"""
@router.post("/auth/authenticate")
async def authenticate(
    auth_request: AuthenticateRequest,
    session: Session = Depends(db.get_db),
    settings: Settings = Depends(get_settings),
):
    logging.info(f"Entering authenticate")
    result = authentication.auth.authenticate(
        session,
        auth_request,
        settings,
    )
    logging.info(f"Got result {result}")
    logging.info(f"Exiting authenticate")
    return result

"""
For testing. Get user's temporary token 
""" 
@router.get("/auth/spoof/{user_id}")
async def spoof_user(
    user_id: int,
    session: Session = Depends(db.get_db),
    settings: Settings = Depends(get_settings),
):
    logging.info(f"Entering spoof_user")
    db_user = session.query(model.User).filter(model.User.id == user_id).first()
    access_token_data: dict = { 
        "sub": db_user.id, 
        "user_id": db_user.id,
        "first_name": db_user.first_name,
        "last_name": db_user.last_name,
    }
    result = authentication.auth.create_access_token(access_token_data, settings)
    logging.info(f"Got result {result}")
    logging.info(f"Exiting spoof_user")
    return result
