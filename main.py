import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel



app = FastAPI()


class User:
    def __init__(self, id: int, email: str, hashed_password: str):
        self.id = id
        self.email = email
        self.hashed_password = hashed_password


class Contact(BaseModel):
    id: int
    user_id: int
    name: str
    email: str

# Приклад бази даних
users_db = {}
rest_app = {}

# Налаштування шифрування паролів
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Налаштування OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Налаштування JWT
SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Функція для хешування пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Функція для генерування токену
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Функція для отримання поточного користувача
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = users_db.get(user_id)
    if user is None:
        raise credentials_exception
    return user

# Реєстрація користувача
@app.post("/register", status_code=201)
async def register(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password
    if email in users_db:
        raise HTTPException(status_code=409, detail="Email already registered")
    hashed_password = pwd_context.hash(password)
    user_id = len(users_db) + 1
    user = User(id=user_id, email=email, hashed_password=hashed_password)
    users_db[user_id] = user
    return {"id": user_id, "email": email}

# Аутентифікація користувача
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Створення контакту
@app.post("/contacts", status_code=201)
async def create_contact(contact: Contact, current_user: User = Depends(get_current_user)):
    contact_id = len(rest_app) + 1
    contact.id = contact_id
    contact.user_id = current_user.id
    rest_app[contact_id] = contact
    return contact

# Отримання контакту
@app.get("/contacts/{contact_id}")
async def read_contact(contact_id: int, current_user: User = Depends(get_current_user)):
    contact = rest_app.get(contact_id)
    if not contact or contact.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)