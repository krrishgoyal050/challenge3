import enum
from datetime import date, datetime
from sqlalchemy import Date, DateTime, Enum, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class ActivityCategory(str, enum.Enum):
    transport = "transport"
    energy = "energy"
    food = "food"
    shopping = "shopping"
    waste = "waste"


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    category: Mapped[ActivityCategory] = mapped_column(Enum(ActivityCategory), index=True)
    activity_type: Mapped[str] = mapped_column(String(80), index=True)
    quantity: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(40))
    emission_kg: Mapped[float] = mapped_column(Float)
    occurred_on: Mapped[date] = mapped_column(Date, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="activities")
