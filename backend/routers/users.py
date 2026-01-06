from fastapi import Depends, HTTPException, Query, Cookie,Response, APIRouter
from typing import Annotated,List,Optional
import bcrypt
from ..models import SQLModel,User,select
from ..dependencies import SessionDep
from ..schemas.user import UserInput,UserRead


router = APIRouter()



@router.post("/", response_model=UserRead, status_code=201)
def create_user(user:UserInput,session:SessionDep):
    existing_user=session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Username exists!")
    if len(user.password)<8:
        raise HTTPException(status_code=400,detail="Weak Password")
    hashed=bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    newusr=User(username=user.username,password_hash=hashed,role="user")
    session.add(newusr)
    session.commit()
    session.refresh(newusr)
    return newusr
