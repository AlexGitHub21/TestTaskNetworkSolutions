from typing import AsyncGenerator
from app.db_session import SessionLocal


async def get_session() -> AsyncGenerator:
    async with SessionLocal() as session:
        yield session