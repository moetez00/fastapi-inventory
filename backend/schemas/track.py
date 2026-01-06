from pydantic import BaseModel,Field,field_validator
from datetime import datetime


class TrackInput(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    artist: str = Field(min_length=1, max_length=200)
    album: str | None = Field(default=None, max_length=200)
    duration_seconds: int = Field(gt=0)

    @field_validator("title", "artist", "album")
    @classmethod
    def strip_strings(cls, v):
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Field cannot be empty")
        return v


class TrackRead(BaseModel):
    id: int
    title: str 
    artist: str 
    album: str|None
    duration_seconds: int
    created_at: datetime 

    class Config:
        from_attributes = True
