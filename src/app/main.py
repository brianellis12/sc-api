from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from csv import DictReader

import uvicorn

from database import crud
from database.db import create_session, run_migrations
from app.geographic_types.routers import router as geographic_type_router
from app.location_data.routers import router as location_data_router     
from app.geographic_types.schema import GeographicTypesCreate
from app.location_data.schema import CensusVariablesCreate

app = FastAPI()

def init_db():
    run_migrations()
    session = create_session()

    # with open("geo_types.csv", 'r', encoding='utf-8-sig') as file:
    #     dict_reader = DictReader(file)
    #     geo_types = list(dict_reader)
    
    # for geo_type in geo_types:
    #     temp = GeographicTypesCreate(
    #         geoid=geo_type['geoid'], longitude=geo_type['longitude'], latitude=geo_type['latitude']
    #     )
    #     crud.geographic_types.create(session, temp)

    temp2 = CensusVariablesCreate(
        name="new name", label="new label", concept="new concetps", group="dhfalkjhdgkajhglkjhdgakljdhflkj"
    )

    crud.census_types.create(session, temp2)

init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(location_data_router)
app.include_router(geographic_type_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)