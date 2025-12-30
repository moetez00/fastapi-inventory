from typing import Annotated,List,Optional
from sqlmodel import Field, SQLModel, Relationship,Session,select
from datetime import datetime
from sqlalchemy.orm import Mapped

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, nullable=False)
    password_hash: str = Field(nullable=False)
    role: str = Field(default="user", nullable=False)

    items: list["Item"] = Relationship(back_populates="owner")
    tokens: list["Token"] = Relationship(back_populates="user")


class Item(SQLModel, table=True):
    __tablename__ = "items"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    qty: int = Field(nullable=False)
    owner_id: int = Field(foreign_key="users.id", nullable=False)

    owner: User = Relationship(back_populates="items")


class Token(SQLModel, table=True):
    __tablename__ = "tokens"

    id: Optional[int] = Field(default=None, primary_key=True)
    token: str = Field(unique=True, nullable=False)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    expires_at: datetime = Field(nullable=False)

    user: User = Relationship(back_populates="tokens")

