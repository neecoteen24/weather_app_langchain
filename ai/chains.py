from ai.llm import get_llm
from ai.prompts import WEATHER_ADVISOR_PROMPT
from ai.output_models import WeatherRecommendation
from models.weather_models import WeatherData
from utils.logger import logger


def format_current_weather(weather: WeatherData) -> str:
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
Temperature: {day.min_temp}°C - {day.max_temp}°C
Rain Chance: {day.rain_chance}%
Humidity: {day.humidity}%
Wind: {day.max_wind} km/h
""".strip()
        )

    return "\n\n".join(lines)


def format_hourly(weather: WeatherData) -> str:
    """
    Include only today's hourly forecast.
    Every 3 hours to reduce token usage.
    """

    if not weather.hourly:
        return "No hourly forecast available."

    lines = []

    today = weather.hourly[0]

    for hour in today.hours[::3]:

        time = hour.time.split(" ")[1]

        lines.append(
            f"{time} | "
            f"{hour.condition} | "
            f"{hour.temperature}°C | "
            f"Rain {hour.rain_chance}%"
        )

    return "\n".join(lines)


def get_weather_recommendation(weather: WeatherData) -> WeatherRecommendation:
    """
    Generate AI recommendations from weather data.
    """

    logger.info(
        "Generating recommendation for %s, %s",
        weather.location.city,
        weather.location.country,
    )

    llm = get_llm().with_structured_output(
        WeatherRecommendation
    )

    chain = WEATHER_ADVISOR_PROMPT | llm

    return chain.invoke(
        {
            "location": f"{weather.location.city}, {weather.location.country}",
            "current_weather": format_current_weather(weather),
            "forecast": format_forecast(weather),
            "hourly_forecast": format_hourly(weather),
        }
    )