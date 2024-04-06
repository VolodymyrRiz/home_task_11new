from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from home_task_11new.db import get_db
from src.schemas import UserBase
from home_task_11new.src.repository import users_0 as repository_users


router = APIRouter(prefix='/users', tags=["users"])


@router.get("/", response_model=List[UserBase])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = await repository_users.get_contacts(skip, limit, db)
    return users


@router.get("/{id}", response_model=UserBase)
async def read_contact(id: int, db: Session = Depends(get_db)):
    user = await repository_users.get_contact(id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=UserBase)
async def create_contact(body: UserBase, db: Session = Depends(get_db)):
    return await repository_users.create_contact(body, db)


@router.put("/{id}", response_model=UserBase)
async def update_contact(body: UserBase,id: int, db: Session = Depends(get_db)):
    user = await repository_users.update_contact(id, body, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


# @router.patch("/{contact_id}", response_model=ContactResponse)
# async def update_status_contact(body: ContactBase, contact_id: int, db: Session = Depends(get_db)):
#     contact = await repository_contacts.update_status_contact(contact_id, body, db)
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
#     return contact


# @router.delete("/{contact_id}", response_model=ContactResponse)
# async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
#     contact = await repository_contacts.remove_contact(contact_id, db)
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
#     return contact