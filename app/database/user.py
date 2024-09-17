from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select

from app.security import get_password_hash
from app.models import User, UserCreate


async def create_user(*, session: AsyncSession, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    await session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def get_user_by_email(*, session: AsyncSession, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_users = await session.exec(statement)
    return session_users[0]
