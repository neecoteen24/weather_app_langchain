from langchain_core.prompts import ChatPromptTemplate

from ai.llm import get_llm
from models.weather_models import WeatherData
from utils.logger import logger


CHAT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an AI Weather Assistant.

The user will ask questions about the supplied weather data.

Rules:

- Answer ONLY using the provided weather information.
- Do not invent weather conditions.
- If the answer cannot be determined from the supplied data,
  politely say that the information is unavailable.
- Keep responses concise.
- Explain your reasoning whenever appropriate.
"""
        ),
        (
            "human",
            """
Location

{location}

Current Weather

{current_weather}

Forecast

{forecast}

Hourly Forecast

{hourly_forecast}

User Question

{question}
"""
        ),
    ]
)


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
Temperature: {day.min_temp}°C - {day.max_temp}°C
Rain Chance: {day.rain_chance}%
Humidity: {day.humidity}%
Wind: {day.max_wind} km/h
""".strip()
        )

    return "\n\n".join(lines)


def format_hourly(weather: WeatherData) -> str:
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


def ask_weather_question(
    weather: WeatherData,
    question: str,
) -> str:
    """
    Answer user questions using the fetched weather data.
    """

    logger.info(
        "Generating chat answer for %s",
        weather.location.city,
    )

    llm = get_llm()

    chain = CHAT_PROMPT | llm

    response = chain.invoke(
        {
            "location": f"{weather.location.city}, {weather.location.country}",
            "current_weather": format_current(weather),
            "forecast": format_forecast(weather),
            "hourly_forecast": format_hourly(weather),
            "question": question,
        }
    )

    logger.info(
        "Chat answer generated for %s",
        weather.location.city,
    )

    return response.content