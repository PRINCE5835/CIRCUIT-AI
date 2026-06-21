from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .health import router as health_router
from .sources import router as sources_router
from .ai import router as ai_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["health"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(sources_router, prefix="/sources", tags=["sources"])
api_router.include_router(ai_router, prefix="/ai", tags=["ai"])
