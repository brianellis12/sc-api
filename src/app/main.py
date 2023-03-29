from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import csv
from app.user.schema import UserCreate

import database.crud as crud
from database.db import create_session, run_migrations
from app.geographic_types.routers import router as geographic_type_router
from app.census_data.routers import router as census_data_router     
from app.census_data.schema import CensusVariablesCreate
from app.user.routers import public as public_user_router, authenticated as authenticated_user_router
from app.authentication.routers import router as auth_router


app = FastAPI()

# Builds the database
def init_db():
    run_migrations()
    session = create_session()

    # Checks if the database is already populated
    existing_rows = crud.CensusTypes.get_all(session)
    if len(existing_rows) > 0:
        return 

    # Adds the csv file with census variables to the database
    with open('census_variables.csv', 'rt') as f:
        csv_reader = csv.reader(f)

        for line in csv_reader:
            temp = CensusVariablesCreate(
                variable=line[0], label=line[1], section=line[2], group=line[3]
            )
            crud.CensusTypes.create(session, temp)

    user = UserCreate(first_name="Brian",last_name="Ellis",email="ellisbxn@gmail.com")
    print(user)
    crud.user.create(session, user)
init_db() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(census_data_router)
app.include_router(geographic_type_router) 
app.include_router(public_user_router)
app.include_router(authenticated_user_router)
app.include_router(auth_router)