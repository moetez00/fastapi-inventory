from fastapi import Depends, FastAPI, HTTPException, Query, Cookie,Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated,List,Optional
import bcrypt
import jwt
from pydantic import BaseModel
from models import SQLModel,User,Item,Token,Session,select
from database import engine
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
app = FastAPI()
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

def get_session():
    with Session(engine) as session:
        yield session
SessionDep = Annotated[Session, Depends(get_session)]


class InputUser(BaseModel):
    username: str
    password: str

@app.post("/users/")
def create_user(user:InputUser,session:SessionDep):
    existing_user=session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username exists!")
    user.password=bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    newusr=User(username=user.username,password_hash=user.password,role="user")
    session.add(newusr)
    session.commit()
    session.refresh(newusr)
    return {"id":newusr.id,"username":newusr.username,"role":newusr.role}

def valid(token:str,session:SessionDep):
    existing_token=session.exec(select(Token).where(Token.token==token)).first()
    if existing_token:
        return True
    else:
        return False

@app.post("/login")
def login(user:InputUser,session:SessionDep,response:Response,access_token:str|None = Cookie(default=None)):
    print(access_token)
    if valid(access_token,session):
        return{"Error":"Already Logged In"}

    existing_user=session.exec(select(User).where(User.username == user.username)).first()
    if (not(existing_user)):
        raise HTTPException(status_code=400, detail="Incorrect Username or Password!")
    if not(bcrypt.checkpw(user.password.encode(), existing_user.password_hash.encode())):
        raise HTTPException(status_code=400, detail="Incorrect Username or Password!")
    

    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    user_id=existing_user.id
    to_encode={"user_id":user_id,"exp":int(expire.timestamp())}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    newtoken=Token(token=encoded_jwt,user_id=user_id,expires_at=expire)
    session.add(newtoken)
    session.commit()
    session.refresh(newtoken)

    response.set_cookie(
        key="access_token",
        value=encoded_jwt,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=60*60*24,
        path="/"
    )

    return {"token":newtoken.token,"exp":newtoken.expires_at}