from pydantic import BaseModel, Field


class RecommendationRead(BaseModel):
    title: str
    description: str
    category: str
    impact_kg: float
    effort: float
    priority_score: float


class AssistantRequest(BaseModel):
    message: str = Field(min_length=2, max_length=2000)


class AssistantResponse(BaseModel):
    answer: str
    recommendations: list[RecommendationRead]
