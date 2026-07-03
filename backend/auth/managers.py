from app.dependencies import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from db.models import User
from sqlalchemy import select


class AuthManager:
    def __init__(self, db_session: AsyncSession = Depends(get_session)) -> None:
        self.db_session = db_session
        self.model = User

    async def get_user_by_username(self, username: str) -> User | None:
        query = select(self.model).where(self.model.username == username)

        result = await self.db_session.execute(query)
        user = result.scalars().one_or_none()
        return user