from fastapi import Depends, HTTPException, Query, Cookie,Response,APIRouter
from typing import Annotated,List,Optional
from ..dependencies import SessionDep
from ..schemas.playlist import PlaylistInput,PlaylistRead
from ..services.playlist import *


router = APIRouter()

@router.get("/")
def createPlaylist(playlist:PlaylistInput,session:SessionDep,access_token:str|None=Cookie(default=None)):
    try:
        createdPlaylist=newPlaylist(playlist,session,access_token)
        