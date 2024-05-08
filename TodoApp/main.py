from fastapi import FastAPI
import models
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# create database command: uvicorn main:app --reload
# pip3 install sqlalchemy
# sqlite3 todo.db