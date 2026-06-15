import streamlit as st

from weather import get_weather
from chains import run_weather_chains

st.set_page_config(
    page_title="AI Weather Assistant"
)

st.title("🌤 AI Weather Assistant")

city = st.text_input(
    "Enter City Name"
)

if st.button("Get Weather"):

    if not city:
        st.warning("Please enter a city name")
    else:
        weather = get_weather(city)

        if weather is None:
            st.error("❌ Could not fetch weather. Check the console for error details.")
        else:

            result = run_weather_chains(weather)

            st.subheader("📍 Current Weather")

            st.write(f"**Location:** {weather['city']}, {weather['country']}")
            st.write(f"**Last Updated:** {weather['last_updated']}")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Temperature", f"{weather['temperature']}°C", f"Feels like {weather['feels_like']}°C")
            with col2:
                st.metric("Humidity", f"{weather['humidity']}%")
            with col3:
                st.metric("Wind Speed", f"{weather['wind_speed']} km/h")
            with col4:
                st.metric("Pressure", f"{weather['pressure_mb']} mb")

            st.write(f"**Condition:** {weather['condition']}")
            st.write(f"**Wind Direction:** {weather['wind_dir']} ({weather['wind_degree']}°)")
            st.write(f"**Cloud Cover:** {weather['cloud']}%")
            st.write(f"**UV Index:** {weather['uv_index']}")

            st.subheader("🤖 Recommendations")

            st.write(result["recommendation"])

    