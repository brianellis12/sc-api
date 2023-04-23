import logging
from fastapi import HTTPException

import jwt
from sqlalchemy.orm import Session

from app.authentication import schema
from app.config import Settings
from app.user import model
from google.oauth2 import id_token
from google.auth.transport import requests

"""
Handles authentication functions
"""
class auth:
    
    """
    Create a unique access token for inputted user
    """
@staticmethod
def authenticate(
    db: Session,
    request: schema.AuthenticateRequest,
    settings: Settings,
):
    logging.info(f"Entering authenticate")
    valid_client_ids = [
        settings.oauth_android_client_id,
        settings.oauth_desktop_client_id,
        settings.oauth_ios_client_id,
        settings.oauth_android_client_id,
        settings.oauth_web_client_id,
    ]
    logging.info(f"Verifying oauth2 token {request.token}")
    idinfo = id_token.verify_oauth2_token(request.token, requests.Request())
    logging.info(f"Got idinfo {idinfo}")

    first_name = ""
    last_name = ""

    if not all(key in idinfo for key in ["given_name", "family_name"]):
        if request.first_name and request.last_name:
            first_name = request.first_name
            last_name = request.last_name
    else:
        first_name = idinfo["given_name"]
        last_name = idinfo["family_name"]

    if not first_name or not last_name:
        logging.info(f"Incomplete token")
        return schema.AuthenticateResponse(incomplete_token=True)

    if idinfo["aud"] not in valid_client_ids:
        logging.error(f"Invalid token")
        raise HTTPException(status_code=401, detail="Invalid token")

    has_email = len(idinfo["email"]) > 0 and idinfo["email_verified"]
    if not has_email:
        logging.error(f"Token has missing/invalid email")
        raise HTTPException(
            status_code=400, detail="Token has missing/invalid email"
        )

    validated_email = idinfo["email"]
    logging.info(f"Querying user by email {validated_email}")
    db_user = (
        db.query(model.User).filter(model.User.email.ilike(validated_email)).first()
    )

    new_user = False
    if db_user is None:
        new_user = True
        logging.info(f"Creating new user with email {validated_email}, first name {first_name}, last name {last_name}")
        db_user = model.User(
            email=validated_email,
            first_name=first_name,
            last_name=last_name,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        access_token_data: dict = {
            "sub": db_user.id,
            "user_id": db_user.id,
            "first_name": db_user.first_name,
            "last_name": db_user.last_name,
        }
        logging.info(f"Creating access token for data {access_token_data}")
        encoded_jwt = auth.create_access_token(access_token_data, settings)
        logging.info(f"Got encoded jwt {encoded_jwt}")

        result = schema.AuthenticateResponse(
            access_token=encoded_jwt,
            user=db_user,
            new_user=new_user,
            incomplete_token=False,
        )
        logging.info(f"Got result {result}")
