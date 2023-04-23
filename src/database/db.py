import logging
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
    logging.info(f"Entering run_migrations")
    logging.info(f"Loading alembic config from ./alembic.ini")
    alembic_cfg = Config("./alembic.ini")
    logging.info(f"Getting engine")
    engine = get_engine()
    with engine.begin() as connection:
        logging.info(f"Setting connection attribute")
        alembic_cfg.attributes["connection"] = connection
        logging.info(f"Running upgrade command")
        command.upgrade(alembic_cfg, "head")
    logging.info(f"Exiting run_migrations")

"""
Creates the engine for SQLAlchemy
"""
def get_engine():
    logging.info(f"Entering get_engine")
    logging.info(f"Getting settings")
    settings = get_settings()
    logging.info(f"Creating engine with connection string {settings.db_connection_string}")
    engine = create_engine(settings.db_connection_string)
    logging.info(f"Got engine {engine}")
    logging.info(f"Exiting get_engine")
    return engine

"""
Creates a database sessions for the API to utilize
"""
def create_session():
    logging.info(f"Entering create_session")
    logging.info(f"Getting engine")
    engine = get_engine()
    logging.info(f"Creating session local with engine {engine}")
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logging.info(f"Creating session with session local {session_local}")
    session = session_local()
    logging.info(f"Got session {session}")
    logging.info(f"Exiting create_session")
    return session

"""
Starts the API's database session
"""
def get_db():
    logging.info(f"Entering get_db")
    logging.info(f"Creating session")
    session = create_session()
    try:
        yield session
    finally:
        logging.info(f"Closing session {session}")
        session.close()
        logging.info(f"Exiting get_db")