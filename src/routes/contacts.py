from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactBase, ContactResponse
from src.repository import contacts as repository_notes


router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = await repository_notes.get_notes(skip, limit, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_note(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_notes.get_note(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse)
async def create_note(body: ContactBase, db: Session = Depends(get_db)):
    return await repository_notes.create_note(body, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_note(body: ContactBase, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_notes.update_note(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.patch("/{contact_id}", response_model=ContactResponse)
async def update_status_note(body: ContactBase, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_notes.update_status_note(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_note(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_notes.remove_note(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

# src/routes/contacts.py

