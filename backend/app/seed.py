import asyncio

from sqlalchemy import select

from app.db_session import SessionLocal
from db.models.user import User
from utils.security import get_password_hash


async def seed_admin():
    async with SessionLocal() as session:

        result = await session.execute(
            select(User).where(User.username == "admin")
        )
        admin = result.scalar_one_or_none()

        if admin:
            print("Admin already exists")
            return

        admin = User(
            username="admin",
            password_hash=get_password_hash("admin"),
            is_admin=True,
        )

        session.add(admin)
        await session.commit()

        print("Admin created")


if __name__ == "__main__":
    asyncio.run(seed_admin())