from fastapi import Depends, FastAPI, HTTPException, Query, Cookie,Response,APIRouter
from typing import Annotated,List,Optional
import bcrypt
import jwt
from sqlmodel import select
from datetime import datetime, timedelta, timezone
from ..models import SQLModel,User,Token
from ..dependencies import SessionDep
from ..schemas.auth import InputUser
from ..services.auth import valid
from ..config import SECRET_KEY
router = APIRouter()


ALGORITHM = "HS256"



@router.post("/")
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