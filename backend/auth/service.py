from fastapi import Depends, HTTPException
from auth.managers import AuthManager
from auth.schemas import AuthUser
from starlette import status
from auth.security import create_access_token
from utils.security import verify_password


class AuthService:
    def __init__(self, manager: AuthManager = Depends(AuthManager)) -> None:
        self.manager = manager

    async def login_admin(self, username: str, password: str) -> dict:
        exist_user = await self.manager.get_user_by_username(username)
        if exist_user is None or not verify_password(
                hashed_password=exist_user.password_hash, raw_password=password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный логин или пароль"
            )

        access_token = create_access_token(
            data={
                "sub": exist_user.username
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }