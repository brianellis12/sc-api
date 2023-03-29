from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
from alembic import command

from app.config import get_settings

base = declarative_base()

"""
Sets database to previously created migrations
"""
def run_migrations():
    alembic_cfg = Config("./alembic.ini")
    engine = get_engine()
    with engine.begin() as connection:
        alembic_cfg.attributes["connection"] = connection
        command.upgrade(alembic_cfg, "head")

"""
Creates the engine for SQLAlchemy
"""
def get_engine():
    settings = get_settings()
    engine = create_engine(settings.db_connection_string)
    return engine

"""
Creates a database sessions for the API to utilize
"""
def create_session():
    engine = get_engine()
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_local()
    return session

"""
Starts the API's database session
"""
def get_db():
    session = create_session()
    try:
        yield session
    finally:
        session.close()