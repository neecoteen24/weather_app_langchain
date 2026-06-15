import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")


def get_weather(city):
    
    if not API_KEY:
        print("ERROR: WEATHER_API_KEY not found in environment variables")
        return None
    
    if not city or city.strip() == "":
        print("ERROR: City name is empty")
        return None

    url = (
        f"https://api.weatherapi.com/v1/current.json"
        f"?key={API_KEY}"
        f"&q={city}"
        f"&aqi=no"
    )

    try:
        response = requests.get(url)

        if response.status_code != 200:
            print(f"ERROR: API returned status {response.status_code}")
            print(f"Response: {response.text}")
            return None

        data = response.json()
        current = data["current"]

        return {
            "city": data["location"]["name"],
            "country": data["location"]["country"],
            "last_updated": current["last_updated"],
            "temperature": current["temp_c"],
            "feels_like": current["feelslike_c"],
            "humidity": current["humidity"],
            "wind_speed": current["wind_kph"],
            "wind_degree": current["wind_degree"],
            "wind_dir": current["wind_dir"],
            "pressure_mb": current["pressure_mb"],
            "precipitation": current["precip_mm"],
            "cloud": current["cloud"],
            "condition": current["condition"]["text"],
            "condition_icon": current["condition"]["icon"],
            "uv_index": current["uv"],
            "is_day": current["is_day"]
        }
    
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Network request failed - {e}")
        return None
    except KeyError as e:
        print(f"ERROR: Missing expected field in API response - {e}")
        return None
    except Exception as e:
        print(f"ERROR: Unexpected error - {e}")
        return None