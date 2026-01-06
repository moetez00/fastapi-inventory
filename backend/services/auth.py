from ..dependencies import SessionDep
from sqlmodel import select,delete
from ..models import Token,User
from datetime import datetime
from ..config import TOKEN_TTL,SECRET_KEY
from ..schemas.auth import UserInput
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone


ALGORITHM = "HS256"


def cleanuptokens(session:SessionDep):
    session.exec(delete(Token).where(Token.expires_at<datetime.utcnow()))
    session.commit()


class InvalidCredentials(Exception):
    pass

def token_exist(token:str,session:SessionDep)->bool:
    return session.exec(select(Token).where(Token.token == token)).first() is not None

def login(user:UserInput,session:SessionDep,access_token:str|None=None):
    cleanuptokens(session)
    if access_token and token_exist(access_token,session):
        session.exec(delete(Token).where(Token.token==access_token))
        session.commit()

    existing_user=session.exec(select(User).where(User.username == user.username)).first()

    if (not(existing_user)) or not(bcrypt.checkpw(user.password.encode(), existing_user.password_hash.encode())):
        raise InvalidCredentials()
    expire = datetime.now(timezone.utc) + timedelta(seconds=TOKEN_TTL)
    user_id=existing_user.id
    to_encode={"user_id":user_id,"exp":int(expire.timestamp())}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    newtoken=Token(token=encoded_jwt,user_id=user_id,expires_at=expire)
    session.add(newtoken)
    session.commit()
    session.refresh(newtoken)
    return encoded_jwt


def logout(session:SessionDep,access_token:str|None=None):
    cleanuptokens(session)
    if access_token and token_exist(access_token,session):
        session.exec(delete(Token).where(Token.token==access_token))
        session.commit()
    
