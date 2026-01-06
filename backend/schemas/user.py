from pydantic import BaseModel

class UserInput(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id:int
    username:str
    role:str