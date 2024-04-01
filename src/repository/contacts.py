from typing import List

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactBase


async def get_notes(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_note(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_note(body: ContactBase, db: Session) -> Contact:
    contact = Contact(first_name=body.first_name, last_name=body.last_name, mail=body.mail, phone=body.phone, birthday=body.birthday, description=body.description)
    
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_note(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_note(contact_id: int, body: ContactBase, db: Session) -> Contact | None:
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


