from datetime import date
from pydantic import BaseModel, Field

from app.models.activity import ActivityCategory


class ActivityCreate(BaseModel):
    category: ActivityCategory
    activity_type: str = Field(min_length=2, max_length=80)
    quantity: float = Field(gt=0, le=100000)
    unit: str = Field(min_length=1, max_length=40)
    occurred_on: date


class ActivityRead(ActivityCreate):
    id: int
    emission_kg: float

    model_config = {"from_attributes": True}


class BreakdownItem(BaseModel):
    category: str
    emission_kg: float


class DashboardRead(BaseModel):
    total_kg: float
    carbon_score: int
    breakdown: list[BreakdownItem]
    trend: list[float]
    spikes: list[int]
    forecast_next_7_days: list[float]
