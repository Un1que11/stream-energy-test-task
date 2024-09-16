from sqlmodel import SQLModel, Session, create_engine

from app import crud
from app.config import settings
from app.models.user.user_model import *
from app.models.note.note_model import *

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But to speed up proccess I decided to create tables by the following approach

    # This works because the models are already imported and registered from app.models
    SQLModel.metadata.create_all(engine)