from pydantic import BaseModel

class InputUser(BaseModel):
    username: str
    password: str
