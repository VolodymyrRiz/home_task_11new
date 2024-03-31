import uvicorn
from fastapi import FastAPI

app = FastAPI()

from fastapi import FastAPI

from src.routes import notes

app = FastAPI()

app.include_router(notes.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

