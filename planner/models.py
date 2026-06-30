from pydantic import BaseModel, Field
from typing import List, Literal


# ---------- INPUT ----------

class PlannerRequest(BaseModel):

    activities: List[str]

    objective: Literal[
        "Stay Comfortable",
        "Stay Dry",
        "Save Time",
        "Exercise",
        "Outdoor Enjoyment",
    ]

    preferred_time: Literal[
        "Morning",
        "Afternoon",
        "Evening",
        "Whole Day",
    ]

    heat_sensitive: bool = False
    cold_sensitive: bool = False
    rain_sensitive: bool = False
    long_commute: bool = False

# ---------- OUTPUT ----------

class ActivityRecommendation(BaseModel):
    activity: str
    score: int = Field(
        ge=1,
        le=10,
        description="Suitability score out of 10."
    )
    decision: Literal[
        "Go",
        "Wait",
        "Avoid"
    ]
    reason: str


class TimelineItem(BaseModel):
    time: str
    recommendation: str


class PlannerOutput(BaseModel):
    summary: str

    activities: List[ActivityRecommendation]

    timeline: List[TimelineItem]

    packing_list: List[str]

    warnings: List[str]