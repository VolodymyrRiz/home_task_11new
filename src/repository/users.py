from typing import List
from auth import Hash
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from src.database.models import User
from src.schemas import UserBase


async def get_contacts(skip: int, limit: int, db: Session) -> List[User]:
    """
    Retrieves a list of contacts for a specific user with specified pagination parameters.
    :param skip: The number of contacts to skip before starting to return contacts.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int    
    :param db: The database session.
    :type db: Session    
    :return: The User with the specified offset, or None if it does not exist.
    :rtype: List[User]
    """
    return db.query(User).offset(skip).limit(limit).all()


async def get_contact(id: int, db: Session) -> User:
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param id: The ID of the contact to retrieve.
    :type id: int   
    :param db: The database session.
    :type db: Session
    :return: The User with the specified ID, or None if it does not exist.
    :rtype: User | None
    """
    return db.query(User).filter(User.id == id).first()


async def create_contact(body: UserBase, db: Session) -> User:
    """
    Creates a new contact for a specific user.

    :param body: The data for the contact to create.
    :type body: UserBase    
    :param db: The database session.
    :type db: Session
    :return: The newly created user.
    :rtype: User
    """
    user = User(email=body.email, password=body.password)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def remove_contact(id: int, db: Session) -> User | None:
    """
    Removes a single contact with the specified ID for a specific user.

    :param id: The ID of the contact to remove.
    :type id: int    
    :param db: The database session.
    :type db: Session
    :return: The removed user, or None if it does not exist.
    :rtype: User | None
    """
    user = db.query(User).filter(User.id == id).first()
    if user:
        db.delete(user)
        db.commit()
    return user


async def get_user_by_email(email: str, db: Session) -> User:
    # Assuming the User model has an 'email' field
    result = db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def confirmed_email(email: str, db: Session) -> None:
    user = get_user_by_email(email, db)
    User.confirmed = True
    db.commit()
    
async def create_user(email: str, password: str, db: Session) -> User:
    user = User(email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

async def hash_handler():
    return Hash()

async def create_access_token(data: dict) -> str:
    return create_access_token(data)

async def verify_password(password: str, hashed_password: str) -> bool:
    return verify_password(password, hashed_password)

async def create_refresh_token(user_id: int, db: Session) -> str:
    refresh_token = create_access_token(data={"sub": user_id})
    return refresh_token

async def update_token(user_id: int, token: str, db: Session) -> None:
    user = db.query(User).filter(User.id == user_id).first()
    user.token = token
    db.commit()

async def repository_users():
    return {
        "get_contacts": get_contacts,
        "get_contact": get_contact,
        "create_contact": create_contact,
        "remove_contact": remove_contact,
        "get_user_by_email": get_user_by_email,
        "confirmed_email": confirmed_email,
        "create_user": create_user, 
        "verify_password": verify_password, 
        "create_refresh_token": create_refresh_token, 
        "update_token": update_token,
    }

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

