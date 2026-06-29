import os
import requests
from dotenv import load_dotenv

load_dotenv()


class WeatherClient:
    """
    Client for communicating with WeatherAPI.

    Responsibility:
        - Make API requests
        - Return raw JSON response
        - Handle HTTP/network errors

    Does NOT:
        - Parse JSON
        - Format data
        - Perform AI processing
    """

    BASE_URL = "https://api.weatherapi.com/v1/forecast.json"

    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY")

        if not self.api_key:
            raise ValueError(
                "WEATHER_API_KEY not found in environment variables."
            )

    def fetch_weather(self, city: str, days: int = 3) -> dict:
        """
        Fetch weather forecast for a city.

        Parameters
        ----------
        city : str
            City name.
        days : int
            Forecast days (1-14 depending on WeatherAPI plan).

        Returns
        -------
        dict
            Raw JSON response from WeatherAPI.

        Raises
        ------
        ValueError
            Invalid city.

        RuntimeError
            API or network error.
        """

        if not city.strip():
            raise ValueError("City name cannot be empty.")

        params = {
            "key": self.api_key,
            "q": city,
            "days": days,
            "aqi": "yes",
            "alerts": "yes",
        }

        try:
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=10
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.HTTPError as e:
            try:
                error = response.json()["error"]["message"]
            except Exception:
                error = str(e)

            raise RuntimeError(f"Weather API Error: {error}")

        except requests.exceptions.Timeout:
            raise RuntimeError("Weather API request timed out.")

        except requests.exceptions.ConnectionError:
            raise RuntimeError(
                "Unable to connect to WeatherAPI."
            )

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Network Error: {e}")