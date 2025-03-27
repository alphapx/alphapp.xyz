from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    **id = Column(Integer, primary_key=True)**
    **username = Column(String(50), unique=True, nullable=False)**
    **email = Column(String(100), unique=True, nullable=False)**
    **password_hash = Column(String(128), nullable=False)**
    **is_active = Column(Boolean, default=True)**

