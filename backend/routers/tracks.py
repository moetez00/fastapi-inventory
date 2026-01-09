from fastapi import Depends, HTTPException, Query, Cookie,Response,APIRouter
from typing import Annotated,List,Optional
from ..dependencies import SessionDep
from ..schemas.track import TrackInput,TrackRead
from ..services.track import *

router = APIRouter()


@router.post("/", response_model=TrackRead, status_code=201)
def createTrack(track:TrackInput,session:SessionDep,access_token:str|None=Cookie(default=None)):
    try:
        createdTrack=newTrack(track,session,access_token)
        return createdTrack
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

@router.get("/")
def listTracks(session:SessionDep,page_size:int=10,page:int=1):
    try:
        return getTracks(session,page_size,page)
    except InvalidPageSize:
        raise HTTPException(status_code=400,detail="Invalid Page Size")
    except InvalidPageNumber:
        raise HTTPException(status_code=400,detail="Invalid Page Number")

@router.delete("/")
def deleteTrack(track:TrackInput,session:SessionDep,access_token:str|None=Cookie(default=None)):
    try:
        return delTrack(track,session,access_token)
    except ForbiddenException:
        raise HTTPException(status_code=403,detail="Forbidden")
    except TrackDoesNotExist:
        raise HTTPException(status_code=403,detail="Track Does Not Exist")
    except FailedDelete:
        raise HTTPException(status_code=403,detail="Failed Delete")
    
