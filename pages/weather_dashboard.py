import streamlit as st

from weather.client import WeatherClient
from weather.parser import WeatherParser

from ai.chains import get_weather_recommendation
from ai.chat import ask_weather_question
from utils.logger import logger
from streamlit_geolocation import streamlit_geolocation


st.set_page_config(
    page_title="AI Weather Assistant",
    page_icon="🌤",
    layout="wide"
)


# ----------------------------
# Session State
# ----------------------------

if "weather" not in st.session_state:
    st.session_state.weather = None

if "recommendation" not in st.session_state:
    st.session_state.recommendation = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "location_mode" not in st.session_state:
    st.session_state.location_mode = "search"

if "geo_location" not in st.session_state:
    st.session_state.geo_location = None

if "city_query" not in st.session_state:
    st.session_state.city_query = ""


# ----------------------------
# Sidebar
# ----------------------------

with st.sidebar:

    st.title("⚙ Settings")

    st.caption("Choose how to look up weather.")

    location_mode = st.radio(
        "Location Source",
        options=["Search city", "Use my location"],
        index=0 if st.session_state.location_mode == "search" else 1,
    )

    st.session_state.location_mode = "search" if location_mode == "Search city" else "geo"

    city = ""

    if st.session_state.location_mode == "search":
        city = st.text_input(
            "City",
            placeholder="Enter city name...",
            key="city_query",
        )
    else:
        st.caption("Allow location access in your browser to use your current position.")
        st.session_state.geo_location = streamlit_geolocation()

        geo_location = st.session_state.geo_location or {}

        latitude = geo_location.get("latitude")
        longitude = geo_location.get("longitude")

        if latitude is not None and longitude is not None:
            st.success(f"Location detected: {latitude:.4f}, {longitude:.4f}")
        else:
            st.info("Waiting for browser location permission...")

    days = st.slider(
        "Forecast Days",
        min_value=1,
        max_value=7,
        value=3
    )

    get_weather = st.button(
        "Get Weather Data",
        use_container_width=True
    )


# ----------------------------
# Header
# ----------------------------

st.title("🌤 AI Weather Assistant")

st.caption(
    "Current weather, forecast analysis and AI-powered recommendations."
)

st.divider()


# ----------------------------
# Fetch Weather
# ----------------------------

if get_weather:

    logger.info(
        "Weather fetch requested mode=%s city=%s days=%s",
        st.session_state.location_mode,
        city,
        days,
    )

    with st.spinner("Fetching weather data..."):

        try:

            client = WeatherClient()

            if st.session_state.location_mode == "geo":
                geo_location = st.session_state.geo_location or {}
                latitude = geo_location.get("latitude")
                longitude = geo_location.get("longitude")

                if latitude is None or longitude is None:
                    raise ValueError(
                        "Location access is required before fetching weather by current location."
                    )

                raw_data = client.fetch_weather_by_coordinates(
                    latitude=latitude,
                    longitude=longitude,
                    days=days,
                )

                logger.info(
                    "Weather API response received for coordinates=(%s, %s)",
                    latitude,
                    longitude,
                )
            else:
                if not city.strip():
                    raise ValueError("Please enter a city name.")

                raw_data = client.fetch_weather(
                    city=city,
                    days=days,
                )

                logger.info("Weather API response received for city=%s", city)

            weather = WeatherParser.parse(raw_data)

            recommendation = get_weather_recommendation(weather)

            logger.info(
                "Weather parsed and recommendation generated for mode=%s",
                st.session_state.location_mode,
            )

            st.session_state.weather = weather
            st.session_state.recommendation = recommendation
            st.session_state.chat_history = []

        except Exception as e:

            logger.exception(
                "Weather workflow failed for mode=%s city=%s",
                st.session_state.location_mode,
                city,
            )

            st.error(str(e))


weather = st.session_state.weather
recommendation = st.session_state.recommendation


# ----------------------------
# Weather Dashboard
# ----------------------------

if weather:

    st.subheader(
        f"📍 {weather.location.city}, {weather.location.country}"
    )

    current = weather.current

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Temperature",
        f"{current.temperature}°C"
    )

    c2.metric(
        "Feels Like",
        f"{current.feels_like}°C"
    )

    c3.metric(
        "Humidity",
        f"{current.humidity}%"
    )

    c4.metric(
        "Wind",
        f"{current.wind_speed} km/h"
    )

    c5, c6, c7 = st.columns(3)

    c5.metric(
        "Pressure",
        f"{current.pressure} mb"
    )

    c6.metric(
        "Visibility",
        f"{current.visibility} km"
    )

    c7.metric(
        "UV Index",
        current.uv
    )

    st.info(
        f"Current Condition: **{current.condition}**"
    )

    st.divider()

    # ------------------------------------
    # Forecast
    # ------------------------------------

    st.subheader("📅 Forecast")

    forecast_table = []

    for day in weather.forecast:

        forecast_table.append({

            "Date": day.date,

            "Condition": day.condition,

            "Min Temp (°C)": day.min_temp,

            "Max Temp (°C)": day.max_temp,

            "Rain %": day.rain_chance,

            "Humidity %": day.humidity,

            "Wind km/h": day.max_wind

        })

    st.dataframe(
        forecast_table,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ------------------------------------
    # Hourly Forecast
    # ------------------------------------

    st.subheader("🕒 Today's Hourly Forecast")

    hourly_table = []

    today = weather.hourly[0]

    for hour in today.hours:

        hourly_table.append({

            "Time": hour.time.split(" ")[1],

            "Condition": hour.condition,

            "Temp (°C)": hour.temperature,

            "Humidity": hour.humidity,

            "Rain %": hour.rain_chance,

            "Wind": hour.wind_speed

        })

    st.dataframe(
        hourly_table,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ------------------------------------
    # AI Recommendations
    # ------------------------------------

    st.subheader("🤖 AI Recommendations")

    with st.expander("📝 Weather Summary", expanded=True):
        st.write(recommendation.summary)

    with st.expander("👕 Clothing"):
        st.write(recommendation.clothing)

    with st.expander("🏃 Outdoor Activities"):
        st.write(recommendation.outdoor)

    with st.expander("🚗 Travel"):
        st.write(recommendation.travel)

    with st.expander("❤️ Health"):
        st.write(recommendation.health)

    if recommendation.warning != "None":

        st.error(
            f"⚠ {recommendation.warning}"
        )

    st.divider()

    # ------------------------------------
    # Chat
    # ------------------------------------

    st.subheader("💬 Ask AI About This Weather")

    question = st.text_input(
        "Ask a question",
        placeholder="Example: Should I carry an umbrella tomorrow?"
    )

    if st.button(
        "Ask AI",
        use_container_width=True
    ):

        if question.strip():

            with st.spinner("Thinking..."):

                logger.info("Weather question asked for city=%s", weather.location.city)

                answer = ask_weather_question(
                    weather,
                    question
                )

                logger.info("Weather question answered for city=%s", weather.location.city)

                st.session_state.chat_history.append(
                    ("You", question)
                )

                st.session_state.chat_history.append(
                    ("AI", answer)
                )

    for sender, message in st.session_state.chat_history:

        if sender == "You":

            st.chat_message("user").write(message)

        else:

            st.chat_message("assistant").write(message)