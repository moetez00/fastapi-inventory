from typing import Annotated,List,Optional
from sqlmodel import Field, SQLModel, Relationship,Session,select
from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy import UniqueConstraint

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, nullable=False)
    password_hash: str = Field(nullable=False)
    role: str = Field(default="user", nullable=False)
    tokens: list["Token"] = Relationship(back_populates="user")


class Track(SQLModel, table=True):
    __tablename__ = "tracks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    artist: str = Field(nullable=False)
    album: str = Field(nullable=True)
    duration_seconds: int = Field( nullable=False)
    created_at: datetime = Field(nullable=False,default_factory=datetime.utcnow)
    playlistsTrack: list["PlaylistTrack"] = Relationship(back_populates="track")

class Playlist(SQLModel,table=True):
    __tablename__="playlists"

    id:Optional[int] = Field(default=None,primary_key=True)
    name: str = Field(nullable=False)
    owner_id: int = Field(nullable=False,foreign_key="users.id")
    is_public: bool = Field(nullable=False,default=False)
    created_at: datetime = Field(nullable=False,default_factory=datetime.utcnow)

    playlistsTrack: list["PlaylistTrack"] = Relationship(back_populates="playlist")

class PlaylistTrack(SQLModel,table=True):
    __tablename__="playlist_tracks"
    __table_args__ = (UniqueConstraint("playlist_id", "position"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    playlist_id:Optional[int] = Field(default=None,foreign_key="playlists.id")
    track_id: int = Field(nullable=False,foreign_key="tracks.id")
    position: int = Field(nullable=False)
    added_at: datetime = Field(default_factory=datetime.utcnow)

    track: Track = Relationship(back_populates="playlistsTrack")
    playlist: Playlist = Relationship(back_populates="playlistsTrack")

class Token(SQLModel, table=True):
    __tablename__ = "tokens"

    id: Optional[int] = Field(default=None, primary_key=True)
    token: str = Field(unique=True, nullable=False)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    expires_at: datetime = Field(nullable=False)

    user: User = Relationship(back_populates="tokens")

