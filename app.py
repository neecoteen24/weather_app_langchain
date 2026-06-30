import streamlit as st

st.set_page_config(
    page_title="AI Weather Assistant",
    page_icon="🌤",
    layout="wide",
)

st.title("🌤 AI Weather Assistant")

st.markdown("""
Welcome to the AI Weather Assistant.

Use the navigation menu on the left to access:

- 🌤 Weather Dashboard
- 🧠 AI Day Planner
- ⚙ Settings
""")

st.info(
    "Fetch weather from the Weather Dashboard first. "
    "The AI Day Planner will reuse that weather data."
)