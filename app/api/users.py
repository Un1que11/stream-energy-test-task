from app.models import UserPublic, UserRegister, UserCreate
from app.common.error import BadRequest
from app.database.db import SessionDep
from app.database.user import get_user_by_email, create_user

from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.post("/signup", response_model=UserPublic)
async def register_user(session: SessionDep, user_in: UserRegister) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = await get_user_by_email(session=session, email=user_in.email)
    if user:
        raise BadRequest(["The user with this email already exists in the system"])
    user_create = UserCreate.model_validate(user_in)
    user = await create_user(session=session, user_create=user_create)
    return user
