from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.routers import get_authenticated_user

from .schema import User, UserCreate, Profile
from typing import List
from database import crud, db, views

public = APIRouter()
authenticated = APIRouter(dependencies=[Depends(get_authenticated_user)])


@public.get("/")
async def root():
    return {"Hello": "World"}


@authenticated.post("/users", response_model=User)
async def add_user(user: UserCreate, session: Session = Depends(db.get_db)):
    return crud.user.create(session, user)


@authenticated.get("/users", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(db.get_db)):
    return crud.user.get_all(db, skip=skip, limit=limit)


@authenticated.get("/users/{user_id}", response_model=User)
async def read_user_by_id(user_id: int, session: Session = Depends(db.get_db)):
    return crud.user.get(session, user_id)


@authenticated.put("/users/{user_id}", response_model=User)
async def update_user(
    user: UserCreate, user_id: int, session: Session = Depends(db.get_db)
):
    return crud.user.update(session, user_id, user)


@authenticated.get("/users/{user_id}/profile", response_model=Profile)
async def get_profile(user_id: int, session: Session = Depends(db.get_db)):
    return views.profile.get(session, user_id)
