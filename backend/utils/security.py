from passlib.context import CryptContext
from app.config import app_settings
from starlette.requests import Request
from fastapi import HTTPException, status


secret = app_settings.secret_key.get_secret_value()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(hashed_password: str, raw_password: str) -> bool:
    return pwd_context.verify(raw_password, hashed_password)

async def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get("Authorization")
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен отсутствует")
    return token