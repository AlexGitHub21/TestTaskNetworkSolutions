from fastapi import APIRouter
from app.routers import ticket_router
from auth.routers import auth_router


apps_router = APIRouter(prefix="/api/v1")

apps_router.include_router(router=ticket_router)
apps_router.include_router(auth_router)