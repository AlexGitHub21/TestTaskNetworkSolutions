from fastapi import APIRouter, Depends
from starlette import status
from auth.service import AuthService
from fastapi.security import OAuth2PasswordRequestForm

from auth.schemas import AuthUser

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post(
    path="/login",
    status_code=status.HTTP_200_OK
)
async def login_admin(form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(AuthService)):
    return await service.login_admin(username=form_data.username, password=form_data.password)