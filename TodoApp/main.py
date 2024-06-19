from fastapi import FastAPI, Depends, Path, status, HTTPException
import models
from database import engine
from routers import auth, todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)

# create database command: uvicorn main:app --reload
# pip3 install sqlalchemy
# sqlite3 todo.db 進入db

