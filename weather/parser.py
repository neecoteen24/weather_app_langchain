from models.weather_models import (
    WeatherData,
    WeatherLocation,
    CurrentWeather,
    ForecastDay,
    HourlyForecast,
    HourlyForecastDay
)


class WeatherParser:
    """
    Converts raw WeatherAPI JSON into our own WeatherData model.
    """

    @staticmethod
    def parse(data: dict) -> WeatherData:

        # ------------------------
        # Location
        # ------------------------

        location = WeatherLocation(
            city=data["location"]["name"],
            country=data["location"]["country"],
            latitude=data["location"]["lat"],
            longitude=data["location"]["lon"],
            timezone=data["location"]["tz_id"],
        )

        # ------------------------
        # Current Weather
        # ------------------------

        current_json = data["current"]

        current = CurrentWeather(
            temperature=current_json["temp_c"],
            feels_like=current_json["feelslike_c"],
            humidity=current_json["humidity"],
            wind_speed=current_json["wind_kph"],
            wind_direction=current_json["wind_dir"],
            pressure=current_json["pressure_mb"],
            uv=current_json["uv"],
            visibility=current_json["vis_km"],
            condition=current_json["condition"]["text"],
            is_day=bool(current_json["is_day"]),
        )

        # ------------------------
        # Forecast
        # ------------------------

        forecast = []

        for day in data["forecast"]["forecastday"]:

            d = day["day"]
            astro = day["astro"]

            forecast.append(
                ForecastDay(
                    date=day["date"],
                    max_temp=d["maxtemp_c"],
                    min_temp=d["mintemp_c"],
                    avg_temp=d["avgtemp_c"],
                    humidity=d["avghumidity"],
                    rain_chance=d["daily_chance_of_rain"],
                    precipitation=d["totalprecip_mm"],
                    max_wind=d["maxwind_kph"],
                    sunrise=astro["sunrise"],
                    sunset=astro["sunset"],
                    condition=d["condition"]["text"],
                )
            )

        # ------------------------
        # Hourly Forecast
        # ------------------------

        hourly_forecasts = []

        for day in data["forecast"]["forecastday"]:

            hours = []

            for hour in day["hour"]:

                hours.append(
                    HourlyForecast(
                        time=hour["time"],
                        temperature=hour["temp_c"],
                        feels_like=hour["feelslike_c"],
                        humidity=hour["humidity"],
                        rain_chance=hour["chance_of_rain"],
                        wind_speed=hour["wind_kph"],
                        uv=hour["uv"],
                        condition=hour["condition"]["text"],
                    )
                )

            hourly_forecasts.append(
                HourlyForecastDay(
                    date=day["date"],
                    hours=hours,
                )
            )

        # ------------------------
        # Final Object
        # ------------------------

        return WeatherData(
            location=location,
            current=current,
            forecast=forecast,
            hourly=hourly_forecasts,
        )