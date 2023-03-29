from sqlalchemy import Column, Integer, String

from database.db import base

"""
User model
"""
class User(base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
