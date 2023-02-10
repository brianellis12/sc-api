from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import db
from app.location_data.routers import router as location_data_router 

db.base.metadata.create_all(bind=db.engine)

# def seed_data():
#     session = db.localSession()   
    

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(location_data_router)