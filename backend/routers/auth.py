from fastapi import Depends, HTTPException, Query, Cookie,Response,APIRouter
from typing import Annotated,List,Optional
from ..dependencies import SessionDep
from ..schemas.auth import UserInput
from ..services.auth import InvalidCredentials,logout as logout_service,login as login_service
from ..config import TOKEN_TTL

router = APIRouter()





@router.post("/login")
def login(user:UserInput,session:SessionDep,response:Response,access_token:str|None = Cookie(default=None)):
    try:
        encoded_jwt=login_service(user,session,access_token)
        response.set_cookie(
            key="access_token",
            value=encoded_jwt,
            httponly=True,
            samesite="lax",
            secure=False,
            max_age=TOKEN_TTL,
            path="/"
        )
        return {"message":"Logged in successfully"}
    except InvalidCredentials:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
@router.post("/logout")
def logout(session:SessionDep,response:Response,access_token:str|None = Cookie(default=None)):
    logout_service(session,access_token)
    response.delete_cookie(
        key="access_token",
        path="/",
        domain=None,
        secure=False,
        samesite="lax",
    )
    return {"message":"Logged out successfully"}