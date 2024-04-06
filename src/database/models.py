from sqlalchemy import Column, Integer, String, Boolean, func, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base
# from pydantic import BaseModel

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    mail = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    birthday = Column(String(50), nullable=False)
    description = Column(String(150), nullable=False)    
    created_at = Column('created_at', DateTime, default=func.now())
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    confirmed = Column(Boolean, default=False)
