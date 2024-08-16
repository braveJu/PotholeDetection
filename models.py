from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    id = Column(String, nullable=False)
    password = Column(String, nullable=False)

class Pothole(Base):
    __tablename__ = "pothole"
    pothole_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    gps_x = Column(Float, nullable=False)
    gpx_y = Column(Float, nullable=False)
    gpx_z = Column(Float, nullable=False)
    discovered_date = Column(DateTime, nullable=False)
    user = relationship("User", backref='user')