from typing import List

from sqlalchemy.orm import Session

from src.database.models import Note
from src.schemas import NoteBase


async def get_notes(skip: int, limit: int, db: Session) -> List[Note]:
    return db.query(Note).offset(skip).limit(limit).all()


async def get_note(note_id: int, db: Session) -> Note:
    return db.query(Note).filter(Note.id == note_id).first()


async def create_note(body: NoteBase, db: Session) -> Note:
    note = Note(first_name=body.first_name, last_name=body.last_name, mail=body.mail, phone=body.phone, birthday=body.birthday, description=body.description)
    
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


async def remove_note(note_id: int, db: Session) -> Note | None:
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        db.delete(note)
        db.commit()
    return note


async def update_note(note_id: int, body: NoteBase, db: Session) -> Note | None:
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        note.first_name = body.first_name
        note.last_name = body.last_name
        note.mail = body.mail
        note.phone = body.phone
        note.birthday = body.birthday
        note.description = body.description
        db.commit()
        
    return note


