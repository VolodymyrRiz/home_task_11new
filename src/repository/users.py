from typing import List

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserBase


async def get_contacts(skip: int, limit: int, db: Session) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


async def get_contact(id: int, db: Session) -> User:
    return db.query(User).filter(User.id == id).first()


async def create_contact(body: UserBase, db: Session) -> User:
    user = User(email=body.email, password=body.password)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def remove_contact(id: int, db: Session) -> User | None:
    user = db.query(User).filter(User.id == id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()



# async def update_contact(contact_id: int, body: ContactBase, db: Session) -> Contact | None:
#     contact = db.query(Contact).filter(Contact.id == contact_id).first()
#     if contact:
#         contact.first_name = body.first_name
#         contact.last_name = body.last_name
#         contact.mail = body.mail
#         contact.phone = body.phone
#         contact.birthday = body.birthday
#         contact.description = body.description
#         db.commit()
        
#     return contact

