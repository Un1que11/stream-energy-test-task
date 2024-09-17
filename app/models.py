import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel, Text, Column, String
from sqlalchemy.dialects import postgresql
from uuid_extensions import uuid7
from utcnow import utcnow


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid7, primary_key=True)
    hashed_password: str
    notes: list["Note"] = Relationship(back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


# Shared properties
class NoteBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Text()
    tags: set[str] | None = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    created_at: str = Field(default=utcnow, nullable=False)
    updated_at: str = Field(default=utcnow, nullable=False)


# Database model, database table inferred from class name
class Note(NoteBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid7, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="notes")


# Properties to receive on item creation
class NoteCreate(NoteBase):
    pass


# Properties to receive on item update
class NoteUpdate(NoteBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Properties to return via API, id is always required
class NotePublic(NoteBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class NotesPublic(SQLModel):
    data: list[NotePublic]
    count: int
