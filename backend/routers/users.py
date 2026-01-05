from fastapi import Depends, HTTPException, Query, Cookie,Response, APIRouter
from typing import Annotated,List,Optional
import bcrypt
from ..models import SQLModel,User,select
from ..dependencies import SessionDep
from ..schemas.auth import InputUser


router = APIRouter()



@router.post("/users/")
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

