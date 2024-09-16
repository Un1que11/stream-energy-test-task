from app.models.user.user_model import User

import uuid

from sqlmodel import SQLModel, Field, Relationship
from uuid_extensions import uuid7



# Shared properties
class NoteBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


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
class ItemPublic(NoteBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int