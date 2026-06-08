from collections import defaultdict
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_session
from app.models.activity import Activity
from app.models.user import User
from app.schemas.recommendation import AssistantRequest, AssistantResponse, RecommendationRead
from app.services.ai import assistant
from app.services.recommendations import build_recommendations, build_sustainability_plan

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


async def _breakdown(session: AsyncSession, user_id: int) -> dict[str, float]:
    result = await session.execute(select(Activity).where(Activity.user_id == user_id))
    totals: dict[str, float] = defaultdict(float)
    for activity in result.scalars():
        totals[activity.category.value] += activity.emission_kg
    return dict(totals)


@router.get("", response_model=list[RecommendationRead])
async def recommendations(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> list[RecommendationRead]:
    ranked = build_recommendations(await _breakdown(session, user.id))
    return [
        RecommendationRead(
            title=item.title,
            description=item.description,
            category=item.category,
            impact_kg=item.impact_kg,
            effort=item.effort,
            priority_score=round(item.priority_score, 2),
        )
        for item in ranked
    ]


@router.get("/plan")
async def sustainability_plan(user: User = Depends(get_current_user)) -> dict[str, object]:
    return build_sustainability_plan()


@router.post("/assistant", response_model=AssistantResponse)
async def chat(
    payload: AssistantRequest,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> AssistantResponse:
    breakdown = await _breakdown(session, user.id)
    recs = await recommendations(session, user)
    answer = await assistant.respond(user.id, payload.message, {"breakdown": breakdown, "recommendations": recs})
    return AssistantResponse(answer=answer, recommendations=recs)
