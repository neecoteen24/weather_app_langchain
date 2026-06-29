import os
import requests

from dotenv import load_dotenv

load_dotenv()


class LocationService:

    BASE_URL = "https://api.weatherapi.com/v1/search.json"

    def __init__(self):

        self.api_key = os.getenv("WEATHER_API_KEY")

        if not self.api_key:
            raise ValueError(
                "WEATHER_API_KEY not found."
            )

    def search_cities(
        self,
        query: str,
        limit: int = 5
    ):
        """
        Search cities using WeatherAPI.

        Returns
        -------
        list[dict]

        Example

        [
            {
                "city":"Kolkata",
                "country":"India",
                "region":"Kolkata"
            }
        ]
        """

        if not query.strip():
            return []

        response = requests.get(
            self.BASE_URL,
            params={
                "key": self.api_key,
                "q": query
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        cities = []

        for city in data[:limit]:

            cities.append(
                {
                    "city": city["name"],
                    "region": city["region"],
                    "country": city["country"],
                    "lat": city["lat"],
                    "lon": city["lon"],
                }
            )

        return cities
    
    def reverse_lookup(self, latitude, longitude):

        client = WeatherClient()

        return client.fetch_weather_by_coordinates(
            latitude,
            longitude,
            days=3,
        )