from datetime import datetime
from pydantic import BaseModel, Field


class ContactBase(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    mail: str = Field(max_length=50)
    phone: str = Field(max_length=50)
    birthday: str = Field(max_length=50)
    description: str = Field(max_length=150)
    
class UserBase(BaseModel):
    email: str = Field(max_length=50)
    password: str = Field(max_length=50)
    
    
class ContactResponse(ContactBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
