from ..dependencies import SessionDep
from sqlmodel import select,delete
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

def createTrack(track:TrackInput,session:SessionDep,access_token:str|None=None):
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
