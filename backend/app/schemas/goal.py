from datetime import date
from pydantic import BaseModel, Field


class GoalCreate(BaseModel):
    title: str = Field(min_length=3, max_length=160)
    target_reduction_kg: float = Field(gt=0)
    start_date: date
    target_date: date


class GoalRead(GoalCreate):
    id: int
    current_reduction_kg: float
    forecast_completion_percent: float

    model_config = {"from_attributes": True}
