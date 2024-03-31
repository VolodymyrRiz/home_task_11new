from datetime import datetime
from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    mail: str = Field(max_length=50)
    phone: str = Field(max_length=50)
    birthday: str = Field(max_length=50)
    description: str = Field(max_length=150)

class NoteResponse(NoteBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
