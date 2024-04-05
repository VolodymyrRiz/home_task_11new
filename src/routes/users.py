from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import UserBase
from src.repository import users as repository_users


router = APIRouter(prefix='/users', tags=["users"])


@router.get("/", response_model=List[UserBase])
async def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = await repository_users.get_notes(skip, limit, db)
    return users


@router.get("/{id}", response_model=UserBase)
async def read_note(id: int, db: Session = Depends(get_db)):
    user = await repository_users.get_note(id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=UserBase)
async def create_note(body: UserBase, db: Session = Depends(get_db)):
    return await repository_users.create_note(body, db)


@router.put("/{id}", response_model=UserBase)
async def update_note(body: UserBase,id: int, db: Session = Depends(get_db)):
    user = await repository_users.update_note(id, body, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


# @router.patch("/{contact_id}", response_model=ContactResponse)
# async def update_status_note(body: ContactBase, contact_id: int, db: Session = Depends(get_db)):
#     contact = await repository_notes.update_status_note(contact_id, body, db)
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
#     return contact


# @router.delete("/{contact_id}", response_model=ContactResponse)
# async def remove_note(contact_id: int, db: Session = Depends(get_db)):
#     contact = await repository_notes.remove_note(contact_id, db)
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
#     return contact