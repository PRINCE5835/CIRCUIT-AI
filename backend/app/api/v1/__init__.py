from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .health import router as health_router
from .sources import router as sources_router
from .ai import router as ai_router
from .projects import router as projects_router
from .circuits import router as circuits_router
from .components import router as components_router
from .marketplace import router as marketplace_router
from .wikipedia import router as wikipedia_router
from .conversations import router as conversations_router
from .files import router as files_router
from .bom import router as bom_router
from .safety import router as safety_router
from .costs import router as costs_router
from .export import router as export_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["health"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(sources_router, prefix="/sources", tags=["sources"])
api_router.include_router(ai_router, prefix="/ai", tags=["ai"])
api_router.include_router(projects_router, prefix="/projects", tags=["projects"])
api_router.include_router(circuits_router, prefix="/circuits", tags=["circuits"])
api_router.include_router(components_router, prefix="/components", tags=["components"])
api_router.include_router(marketplace_router, prefix="/marketplace", tags=["marketplace"])
api_router.include_router(wikipedia_router, tags=["wikipedia"])
api_router.include_router(conversations_router, prefix="/conversations", tags=["conversations"])
api_router.include_router(files_router, prefix="/files", tags=["files"])
api_router.include_router(bom_router, prefix="/projects", tags=["bom"])
api_router.include_router(safety_router, prefix="/safety-reports", tags=["safety"])
api_router.include_router(costs_router, prefix="/cost-estimates", tags=["costs"])
api_router.include_router(export_router, tags=["export"])
