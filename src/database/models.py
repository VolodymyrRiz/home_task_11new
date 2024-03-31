from sqlalchemy import Column, Integer, String, Boolean, func, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    mail = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    birthday = Column(String(50), nullable=False)
    description = Column(String(150), nullable=False)    
    created_at = Column('created_at', DateTime, default=func.now())
