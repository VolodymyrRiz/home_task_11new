from typing import List

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactBase
from sqlalchemy import select


async def get_contacts(limit: int, offset: int, db: Session, current_user: User):
    stmt = select(Contact).filter_by(user=current_user).offset(offset).limit(limit)
    contact = await db.execute(stmt)
    return contact.scalars().all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactBase, db: Session) -> Contact:
    contact = Contact(first_name=body.first_name, last_name=body.last_name, mail=body.mail, phone=body.phone, birthday=body.birthday, description=body.description)
    
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactBase, db: Session) -> Contact | None:
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


