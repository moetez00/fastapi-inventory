from fastapi import FastAPI
from .database import engine
from .config import *
from .routers import users_router,auth_router
from .models import *
from sqlmodel import SQLModel

app = FastAPI()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(users_router,prefix="/users",tags=["users"])

app.include_router(auth_router,prefix="/login",tags=["login"])
