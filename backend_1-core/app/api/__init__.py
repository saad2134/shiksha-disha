# API routes
from .users import router as users_router
from .actions import router as actions_router
from .notifications import router as notifications_router
from .behavior import router as behavior_router
from .streak import router as streak_router

__all__ = [
    "users_router",
    "actions_router", 
    "notifications_router",
    "behavior_router",
    "streak_router"
]
