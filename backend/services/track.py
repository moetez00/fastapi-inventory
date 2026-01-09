from ..dependencies import SessionDep
from sqlmodel import select,delete,func
from ..models import Track,User
from datetime import datetime
from ..schemas.track import TrackInput,TrackRead
from datetime import datetime, timedelta, timezone
from ..config import SECRET_KEY,ALGORITHM
import jwt

class ForbiddenException(Exception):
    pass
class InvalidTitle(Exception):
    pass
class InvalidArtist(Exception):
    pass
class InvalidDuration(Exception):
    pass
class TrackExist(Exception):
    pass
class InvalidPageSize(Exception):
    pass
class InvalidPageNumber(Exception):
    pass
class TrackDoesNotExist(Exception):
    pass
class FailedDelete(Exception):
    pass

def isAdmin(session:SessionDep,access_token:str|None=None):
    if access_token is None:
        return False
    user_id=jwt.decode(access_token,SECRET_KEY, algorithms=[f"{ALGORITHM}"])["user_id"]
    if user_id is None:
        return False
    user = session.get(User, user_id)
    if not user:
        return False
    return user.role == "admin"

def exist(title:str,artist:str,session:SessionDep):
    a= session.exec(select(Track).where(Track.title==title,Track.artist==artist)).first()
    if a:
        return True
    else:
        return False

def newTrack(track:TrackInput,session:SessionDep,access_token:str|None=None):
    if not(isAdmin(session,access_token)):
        raise ForbiddenException()
    if len(track.title)==0:
        raise InvalidTitle()
    if len(track.artist)==0:
        raise InvalidArtist()
    if track.duration_seconds<=0:
        raise InvalidDuration()
    if exist(track.title,track.artist,session):
        raise TrackExist()

    newTrack=Track(
        title=track.title,
        artist=track.artist,
        album=track.album,
        duration_seconds=track.duration_seconds,
        created_at=datetime.utcnow()
        )
    session.add(newTrack)
    session.commit()
    session.refresh(newTrack)
    return newTrack


def getTracks(session:SessionDep,page_size:int=10,page:int=1):
    if(not(0<page_size<=30)):
        raise InvalidPageSize()
    total_count=session.execute(select(func.count()).select_from(Track)).scalar()
    total_pages=total_count//page_size
    if (total_count%page_size!=0):
        total_pages+=1
    if(page<=0 or (not(page<=total_pages) and total_count!=0)):
        raise InvalidPageNumber()
    tracks=session.scalars(select(Track).offset((page-1)*page_size).order_by(Track.id).limit(page_size)).all()
    return {"tracks":tracks,"page":page,"page_size":page_size,"total_pages":total_pages,"total_count":total_count}

def delTrack(track:TrackInput,session:SessionDep,access_token:str):
    if not(isAdmin(session,access_token)):
        raise ForbiddenException()
    if not(exist(track.title,track.artist,session)):
        raise TrackDoesNotExist()
    session.exec(delete(Track).where(Track.title==track.title,Track.artist==track.artist,Track.album==track.album,Track.duration_seconds==track.duration_seconds))
    session.commit()
    if (exist(track.title,track.artist,session)):
        raise FailedDelete()
    else:
        return {"message":"Track has been deleted successfully!"}