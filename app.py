import streamlit as st

from weather.client import WeatherClient
from weather.parser import WeatherParser

from ai.chains import get_weather_recommendation
from ai.chat import ask_weather_question


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


# ----------------------------
# Sidebar
# ----------------------------

with st.sidebar:

    st.title("⚙ Settings")

    city = st.text_input(
        "City",
        placeholder="Enter city name..."
    )

    days = st.slider(
        "Forecast Days",
        min_value=1,
        max_value=7,
        value=3
    )

    get_weather = st.button(
        "Get Forecast",
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

    with st.spinner("Fetching weather data..."):

        try:

            client = WeatherClient()

            raw_data = client.fetch_weather(
                city=city,
                days=days
            )

            weather = WeatherParser.parse(raw_data)

            recommendation = get_weather_recommendation(weather)

            st.session_state.weather = weather
            st.session_state.recommendation = recommendation
            st.session_state.chat_history = []

        except Exception as e:

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

                answer = ask_weather_question(
                    weather,
                    question
                )

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