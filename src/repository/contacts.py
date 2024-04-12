from typing import List

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactBase
from sqlalchemy import select


async def get_contacts(limit: int, offset: int, db: Session, current_user: User):
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
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    stmt = select(Contact).filter_by(user=current_user).offset(offset).limit(limit)
    contact = db.execute(stmt)
    return contact.scalars().all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int   
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactBase, db: Session) -> Contact:
    """
    Creates a new contact for a specific user.

    :param body: The data for the contact to create.
    :type body: ContactBase    
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contact
    """
    contact = Contact(first_name=body.first_name, last_name=body.last_name, mail=body.mail, phone=body.phone, birthday=body.birthday, description=body.description)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int    
    :param db: The database session.
    :type db: Session
    :return: The removed contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactBase, db: Session) -> Contact | None:
    """
    Updates a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The updated data for the contact.
    :type body: ContactBase    
    :param db: The database session.
    :type db: Session
    :return: The updated contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.mail = body.mail
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
        
    return contact


