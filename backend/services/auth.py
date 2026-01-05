
from fastapi import Depends, FastAPI, HTTPException, Query, Cookie,Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated,List,Optional
import bcrypt
import jwt
from backend.models import SQLModel,User,Token
from backend.dependencies import SessionDep



def valid(token:str,session:SessionDep):
    existing_token=session.exec(select(Token).where(Token.token==token)).first()
    if existing_token:
        return True
    else:
        return False
