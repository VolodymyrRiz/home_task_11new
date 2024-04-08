from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from starlette import status


from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks, Request
from src.schemas import UserModel, UserResponse, TokenModel, RequestEmail

from db import get_db
from sqlalchemy.orm import Session
# from src.services.email import send_email
# from src.repository.users import repository_users
from fastapi.security import OAuth2PasswordRequestForm

from datetime import datetime, timedelta
from typing import Optional

from src.database.models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from starlette import status


SECRET_KEY = "secret_key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def auth_service():
    SECRET_KEY = "secret_key"
    return SECRET_KEY
    
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload["sub"]
        if email is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception

    user: User = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user



async def create_email_token(self, data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"iat": datetime.utcnow(), "exp": expire})
    token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
    return token

async def get_email_from_token(self, token: str):
  try:
      payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
      email = payload["sub"]
      return email
  except JWTError as e:
      print(e)
      raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                          detail="Invalid token for email verification")

