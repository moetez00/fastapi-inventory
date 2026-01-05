from ..dependencies import SessionDep
from sqlmodel import select
from ..models import Token



def valid(token:str,session:SessionDep):
    existing_token=session.exec(select(Token).where(Token.token==token)).first()
    if existing_token:
        return True
    else:
        return False
