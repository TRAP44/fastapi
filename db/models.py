from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from .connect import Base

class User(Base):
    __tablename__ = "users"


    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))