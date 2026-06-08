from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_session
from app.models.goal import Goal
from app.models.user import User
from app.schemas.goal import GoalCreate, GoalRead
from app.services.prediction import forecast_goal_completion

router = APIRouter(prefix="/goals", tags=["goals"])


@router.post("", response_model=GoalRead, status_code=201)
async def create_goal(
    payload: GoalCreate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> GoalRead:
    if payload.target_date <= payload.start_date:
        raise HTTPException(status_code=422, detail="target_date must be after start_date")
    goal = Goal(user_id=user.id, **payload.model_dump())
    session.add(goal)
    await session.commit()
    await session.refresh(goal)
    return _read(goal)


@router.get("", response_model=list[GoalRead])
async def list_goals(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> list[GoalRead]:
    result = await session.execute(select(Goal).where(Goal.user_id == user.id))
    return [_read(goal) for goal in result.scalars()]


def _read(goal: Goal) -> GoalRead:
    today = date.today()
    return GoalRead(
        id=goal.id,
        title=goal.title,
        target_reduction_kg=goal.target_reduction_kg,
        current_reduction_kg=goal.current_reduction_kg,
        start_date=goal.start_date,
        target_date=goal.target_date,
        forecast_completion_percent=forecast_goal_completion(
            goal.current_reduction_kg,
            goal.target_reduction_kg,
            max((today - goal.start_date).days, 1),
            max((goal.target_date - goal.start_date).days, 1),
        ),
    )
