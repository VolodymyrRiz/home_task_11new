from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from db import get_db
from src.schemas import UserBase
from src.repository.users import get_contacts, get_contact, create_contact



router = APIRouter(prefix='/users', tags=["users"])


@router.get("/", response_model=List[UserBase])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Reads a list of contacts for a specific user.
    :param skip: The number of contacts to skip before starting to return contacts.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int    
    :param db: The database session.
    :type db: Session    
    :return: users.
    :rtype: List[User]
    """
    users = get_contacts(skip, limit, db)
    return users


@router.get("/{id}", response_model=UserBase)
async def read_contact(id: int, db: Session = Depends(get_db)):
    """
    Reads a single contact with the specified ID for a specific user.

    :param id: The ID of the contact to retrieve.
    :type id: int   
    :param db: The database session.
    :type db: Session
    :return: user.
    :rtype: User | None
    """
    user = get_contact(id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=UserBase)
async def create_contact(body: UserBase, db: Session = Depends(get_db)):
    """
    Creates a new contact for a specific user.

    :param body: The data for the contact to create.
    :type body: UserBase    
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contact
    """
    return create_contact(body, db)


@router.put("/{id}", response_model=UserBase)
async def update_contact(body: UserBase, id: int, db: Session = Depends(get_db)):
    """
    Updates a single contact with the specified ID for a specific user.
    
    :param body: The updated data for the contact.
    :type body: UserBase    
    :param id: The ID of the contact to update.
    :type id: int    
    :param db: The database session.
    :type db: Session
    :return: user.
    :rtype: User | None
    """
    user = update_contact(id, body, db)
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