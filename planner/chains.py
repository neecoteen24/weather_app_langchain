from ai.llm import get_llm

from planner.models import (
    PlannerRequest,
    PlannerOutput
)

from planner.prompts import PLANNER_PROMPT

from models.weather_models import WeatherData


def format_current(weather: WeatherData) -> str:

    current = weather.current

    return f"""
Condition: {current.condition}
Temperature: {current.temperature}°C
Feels Like: {current.feels_like}°C
Humidity: {current.humidity}%
Wind Speed: {current.wind_speed} km/h
Pressure: {current.pressure} mb
Visibility: {current.visibility} km
UV Index: {current.uv}
""".strip()


def format_forecast(weather: WeatherData) -> str:

    lines = []

    for day in weather.forecast:

        lines.append(
            f"""
Date: {day.date}

Condition: {day.condition}

Temperature:
{day.min_temp}°C - {day.max_temp}°C

Rain Chance:
{day.rain_chance}%

Humidity:
{day.humidity}%

Wind:
{day.max_wind} km/h
""".strip()
        )

    return "\n\n".join(lines)


def format_hourly(weather: WeatherData) -> str:

    if not weather.hourly:
        return "No hourly forecast."

    today = weather.hourly[0]

    lines = []

    for hour in today.hours[::3]:

        lines.append(
            f"""
{hour.time}

{hour.condition}

Temp:
{hour.temperature}°C

Rain:
{hour.rain_chance}%
""".strip()
        )

    return "\n".join(lines)


def generate_daily_plan(
    weather: WeatherData,
    request: PlannerRequest,
) -> PlannerOutput:

    llm = get_llm().with_structured_output(
        PlannerOutput
    )

    chain = PLANNER_PROMPT | llm

    return chain.invoke(

        {

            "location":
                f"{weather.location.city}, {weather.location.country}",

            "current_weather":
                format_current(weather),

            "forecast":
                format_forecast(weather),

            "hourly_forecast":
                format_hourly(weather),

            "activities":
                ", ".join(request.activities),

            "preferred_time":
                request.preferred_time,

            "heat_sensitive":
                request.heat_sensitive,

            "cold_sensitive":
                request.cold_sensitive,

            "rain_sensitive":
                request.rain_sensitive,

            "long_commute":
                request.long_commute,

        }

    )