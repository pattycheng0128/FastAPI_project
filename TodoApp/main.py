from fastapi import FastAPI, Depends, Path, status, HTTPException
import models
from database import engine
from routers import auth, todos, admin, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

# create database command: uvicorn main:app --reload
# pip3 install sqlalchemy
# sqlite3 todosapp.db 進入db

