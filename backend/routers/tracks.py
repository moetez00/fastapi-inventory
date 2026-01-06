from fastapi import Depends, FastAPI, HTTPException, Query, Cookie,Response,APIRouter
from typing import Annotated,List,Optional
from ..dependencies import SessionDep
from ..schemas.track import TrackInput,TrackRead
from ..services.track import ForbiddenException,InvalidTitle,InvalidArtist,InvalidDuration,createTrack,TrackExist

router = APIRouter()


@router.post("/", response_model=TrackRead, status_code=201)
def newTrack(track:TrackInput,session:SessionDep,access_token:str|None=Cookie(default=None)):
    try:
        newTrack=createTrack(track,session,access_token)
        return newTrack
    except ForbiddenException:
        raise HTTPException(status_code=403,detail="Forbidden")
    except InvalidTitle:
        raise HTTPException(status_code=400,detail="Invalid Title")
    except InvalidArtist:
        raise HTTPException(status_code=400,detail="Invalid Artist")
    except InvalidDuration:
        raise HTTPException(status_code=400,detail="Invalid Duration")
    except TrackExist:
        raise HTTPException(status_code=409,detail="Track Exists")
