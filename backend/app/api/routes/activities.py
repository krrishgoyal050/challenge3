from collections import defaultdict
from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.algorithms.carbon_factors import get_factor_store
from app.algorithms.trends import detect_spikes
from app.core.security import get_current_user
from app.db.session import get_session
from app.models.activity import Activity
from app.models.user import User
from app.schemas.activity import ActivityCreate, ActivityRead, BreakdownItem, DashboardRead
from app.services.prediction import linear_regression_forecast

router = APIRouter(prefix="/activities", tags=["activities"])


@router.post("", response_model=ActivityRead, status_code=201)
async def create_activity(
    payload: ActivityCreate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> Activity:
    factor = get_factor_store().lookup(payload.activity_type, payload.unit)
    activity = Activity(
        user_id=user.id,
        category=payload.category,
        activity_type=payload.activity_type.lower(),
        quantity=payload.quantity,
        unit=payload.unit.lower(),
        emission_kg=round(payload.quantity * factor, 3),
        occurred_on=payload.occurred_on,
    )
    session.add(activity)
    await session.commit()
    await session.refresh(activity)
    return activity


@router.get("", response_model=list[ActivityRead])
async def list_activities(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> list[Activity]:
    result = await session.execute(select(Activity).where(Activity.user_id == user.id).order_by(Activity.occurred_on.desc()))
    return list(result.scalars())


@router.get("/dashboard", response_model=DashboardRead)
async def dashboard(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> DashboardRead:
    result = await session.execute(select(Activity).where(Activity.user_id == user.id))
    activities = list(result.scalars())
    breakdown: dict[str, float] = defaultdict(float)
    daily: dict[date, float] = defaultdict(float)
    for activity in activities:
        breakdown[activity.category.value] += activity.emission_kg
        daily[activity.occurred_on] += activity.emission_kg

    today = date.today()
    trend = [round(daily.get(today - timedelta(days=idx), 0.0), 2) for idx in range(29, -1, -1)]
    total = round(sum(breakdown.values()), 2)
    score = max(0, min(100, int(100 - total / 20)))
    return DashboardRead(
        total_kg=total,
        carbon_score=score,
        breakdown=[BreakdownItem(category=key, emission_kg=round(value, 2)) for key, value in breakdown.items()],
        trend=trend,
        spikes=detect_spikes(trend),
        forecast_next_7_days=linear_regression_forecast(trend, 7),
    )
