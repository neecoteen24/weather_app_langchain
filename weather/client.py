import os
import requests
from dotenv import load_dotenv

from utils.logger import logger

load_dotenv()


class WeatherClient:

    BASE_URL = "https://api.weatherapi.com/v1/forecast.json"

    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY")

        if not self.api_key:
            raise ValueError("WEATHER_API_KEY not found.")

    def _request_weather(self, query: str, days: int = 3) -> dict:

        logger.info("Calling WeatherAPI with query=%s", query)

        params = {
            "key": self.api_key,
            "q": query,
            "days": days,
            "aqi": "yes",
            "alerts": "yes",
            "lang": "en",
        }

        try:

            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=10,
            )

            response.raise_for_status()

            logger.info("WeatherAPI request successful.")

            return response.json()

        except requests.exceptions.HTTPError as e:

            try:
                error = response.json()["error"]["message"]
            except Exception:
                error = str(e)

            logger.exception("WeatherAPI HTTP error")

            raise RuntimeError(error)

        except requests.exceptions.Timeout:

            logger.exception("WeatherAPI timeout")

            raise RuntimeError("Weather API timed out.")

        except requests.exceptions.ConnectionError:

            logger.exception("WeatherAPI connection error")

            raise RuntimeError("Unable to connect to WeatherAPI.")

        except requests.exceptions.RequestException as e:

            logger.exception("WeatherAPI request failed")

            raise RuntimeError(str(e))

    def fetch_weather(self, city: str, days: int = 3):

        if not city.strip():
            raise ValueError("City cannot be empty.")

        return self._request_weather(city, days)

    def fetch_weather_by_coordinates(
        self,
        latitude: float,
        longitude: float,
        days: int = 3,
    ):

        query = f"{latitude},{longitude}"

        return self._request_weather(query, days)