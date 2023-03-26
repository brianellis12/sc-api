from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.devices.model import Device

from database.db import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    practice_area = Column(String, default="", nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    registered_devices = relationship(Device)
