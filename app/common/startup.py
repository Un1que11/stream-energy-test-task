from app.database.db import connect_and_init_db


async def startup():
    await connect_and_init_db()