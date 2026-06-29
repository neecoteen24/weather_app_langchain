from pydantic import BaseModel, Field


class WeatherRecommendation(BaseModel):
    """
    Structured response returned by the AI Weather Assistant.
    """

    summary: str = Field(
        description="Overall summary of the weather and forecast."
    )

    clothing: str = Field(
        description="Recommended clothing based on the weather."
    )

    outdoor: str = Field(
        description="Recommendation for outdoor activities."
    )

    travel: str = Field(
        description="Travel advice considering the forecast."
    )

    health: str = Field(
        description="Health and safety advice based on the weather."
    )

    warning: str = Field(
        description="Important weather warnings. Return 'None' if there are no significant warnings."
    )