# API endpoints package
from .auth import router as auth_router
from .celebrities import router as celebrities_router
from .votes import router as votes_router

__all__ = ["auth_router", "celebrities_router", "votes_router"] 