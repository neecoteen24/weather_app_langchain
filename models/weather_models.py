from pydantic import BaseModel
from typing import List


class WeatherLocation(BaseModel):
    city: str
    country: str
    latitude: float
    longitude: float
    timezone: str


class CurrentWeather(BaseModel):
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    wind_direction: str
    pressure: float
    uv: float
    visibility: float
    condition: str
    is_day: bool


class ForecastDay(BaseModel):
    date: str
    max_temp: float
    min_temp: float
    avg_temp: float
    humidity: int
    rain_chance: int
    precipitation: float
    max_wind: float
    sunrise: str
    sunset: str
    condition: str


class HourlyForecast(BaseModel):
    time: str
    temperature: float
    feels_like: float
    humidity: int
    rain_chance: int
    wind_speed: float
    uv: float
    condition: str


class HourlyForecastDay(BaseModel):
    date: str
    hours: List[HourlyForecast]


class WeatherData(BaseModel):
    location: WeatherLocation
    current: CurrentWeather
    forecast: List[ForecastDay]
    hourly: List[HourlyForecastDay]