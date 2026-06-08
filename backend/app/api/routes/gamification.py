from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/gamification", tags=["gamification"])


@router.get("/profile")
async def gamification_profile(user: User = Depends(get_current_user)) -> dict[str, object]:
    return {
        "user": user.name,
        "points": 1280,
        "level": "Carbon Cutter",
        "badges": ["First Log", "Transit Tryout", "Waste Watcher"],
        "challenges": [
            {"title": "Low-carbon commute week", "reward_points": 200, "progress": 60},
            {"title": "Three plant-forward dinners", "reward_points": 150, "progress": 33},
        ],
        "leaderboard": [
            {"name": user.name, "points": 1280},
            {"name": "Avery", "points": 1190},
            {"name": "Mina", "points": 1055},
        ],
    }
