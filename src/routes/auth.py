from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request
from src.schemas import UserModel, UserResponse, TokenModel, RequestEmail
#from src.services.auth import auth_service
from src.services.auth import get_email_from_token
from src.services.auth import get_password_hash
#, get_user_by_email, create_user, verify_password, create_refresh_token, update_token, confirmed_email
from db import get_db
from sqlalchemy.orm import Session
from src.services.email import send_email
from src.repository.users import repository_users
from fastapi.security import OAuth2PasswordRequestForm
from src.repository.users import get_user_by_email, create_user, verify_password, create_refresh_token, update_token, confirmed_email
from datetime import datetime, timedelta
from typing import Optional

from src.database.models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from starlette import status

from src.schemas import TokenModel

#from dependencies import get_current_active_user




router = APIRouter(prefix='/auth', tags=["auth"])

class Hash:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)


SECRET_KEY = "secret_key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# define a function to generate a new access token
async def create_access_token(data: dict, expires_delta: Optional[float] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    exist_user = get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = get_password_hash(body.password)
    new_user = create_user(body, db)
    background_tasks.add_task(send_email, new_user.email, request.base_url)
    return {"user": new_user, "detail": "User successfully created. Check your email for confirmation."}

@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not User.confirmed:  # Assuming there's a 'confirmed' attribute on the User model
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not verify_password(body.password, User.password):  # Assuming 'password' is a field on the User model
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = create_access_token(User.id, User.email)  # Pass the user's email as the identity
    refresh_token = create_refresh_token(User.id, User.email)  # Pass the user's email as the identity
    update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    email = get_email_from_token(token)
    user = get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if User.confirmed:
        return {"message": "Your email is already confirmed"}
    confirmed_email(email, db)
    return {"message": "Email confirmed"}



@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):
    user = get_user_by_email(body.email, db)

    if User.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, User.email, request.base_url)
    return {"message": "Check your email for confirmation."}

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
