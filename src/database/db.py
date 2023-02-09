from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

URL = "postgresql://postgres:password@db:5432/data_maps"
engine = create_engine(URL)

localSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()

def get_db():
    session = localSession()
    try:
        yield session
    finally:
        session.close()