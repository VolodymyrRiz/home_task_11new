from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.database.models import User
from db import get_db
from src.schemas import ContactBase, ContactResponse
from src.repository import contacts as repository_contacts

from fastapi import Query
# from src.services.auth import auth_service
from src.routes.auth import get_current_user




router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=list[ContactResponse])
async def get_contacts(
    limit: int = Query(10, ge=10, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
):
    """
    Retrieves a list of contacts for a specific user with specified pagination parameters.

    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param offset: The number of contacts to skip before starting to return contacts.
    :type offset: int
    :param db: The database session.
    :type db: Session
    :param current_user: The user to retrieve contacts for.
    :type current_user: User    
    :return: contacts.
    :rtype: List[Contact]
    """
    contacts = repository_contacts.get_contacts(limit, offset, db, current_user)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    Reads a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int   
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactBase, db: Session = Depends(get_db)):
    """
    Creates a new contact for a specific user.

    :param body: The data for the contact to create.
    :type body: ContactBase    
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contact
    """
    return repository_contacts.create_contact(body, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactBase, contact_id: int, db: Session = Depends(get_db)):
    """
    Updates a single contact with the specified ID for a specific user.
   
    :param body: The updated data for the contact.
    :type body: ContactBase    
    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :return: contact.
    :rtype: Contact | None
    """
    contact = repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.patch("/{contact_id}", response_model=ContactResponse)
async def update_status_contact(body: ContactBase, contact_id: int, db: Session = Depends(get_db)):
    contact = update_status_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int    
    :param db: The database session.
    :type db: Session
    :return: The removed contact.
    :rtype: Contact | None
    """
    contact = repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

# src/routes/contacts.py

