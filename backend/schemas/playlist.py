from pydantic import BaseModel,Field,field_validator
from datetime import datetime


class TrackInput(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    is_public: bool = Field(default=False)

    @field_validator("name", "is_public")
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
    name: str 
    owner_id: int 
    is_public: bool
    created_at: datetime 

    class Config:
        from_attributes = True
