from app.database.db import init_db


async def startup():
    await init_db()
