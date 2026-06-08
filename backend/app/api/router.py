from fastapi import APIRouter, Depends

from app.api.deps import rate_limiter
from app.api.routes import activities, auth, gamification, goals, recommendations

api_router = APIRouter(dependencies=[Depends(rate_limiter)])
api_router.include_router(auth.router)
api_router.include_router(activities.router)
api_router.include_router(recommendations.router)
api_router.include_router(goals.router)
api_router.include_router(gamification.router)
