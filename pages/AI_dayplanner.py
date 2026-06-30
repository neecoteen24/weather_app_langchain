import streamlit as st

from planner.models import PlannerRequest
from planner.chains import generate_daily_plan
from planner.constants import ACTIVITIES

st.set_page_config(
    page_title="AI Day Planner",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 AI Day Planner")

st.caption(
    "Generate a personalized plan based on today's weather and your activities."
)

# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "planner_output" not in st.session_state:
    st.session_state.planner_output = None

weather = st.session_state.get("weather")

if weather is None:
    st.warning(
        "No weather data found.\n\n"
        "Please visit the Weather Dashboard first and fetch the weather."
    )
    st.stop()

# ---------------------------------------------------
# Sidebar Inputs
# ---------------------------------------------------

with st.sidebar:

    st.header("Today's Plan")

    activities = st.multiselect(
        "Activities",
        ACTIVITIES,
        placeholder="Select one or more activities...",
    )

    preferred_time = st.radio(
        "Preferred Time",
        [
            "Morning",
            "Afternoon",
            "Evening",
            "Whole Day",
        ],
    )

    objective = st.selectbox(
        "Today's Objective",
        [
            "Stay Comfortable",
            "Stay Dry",
            "Save Time",
            "Exercise",
            "Outdoor Enjoyment",
        ],
    )

    st.divider()

    st.subheader("Preferences")

    heat_sensitive = st.checkbox("Heat Sensitive")

    cold_sensitive = st.checkbox("Cold Sensitive")

    rain_sensitive = st.checkbox("Rain Sensitive")

    long_commute = st.checkbox("Long Commute")

    generate = st.button(
        "Generate Plan",
        use_container_width=True,
    )

# ---------------------------------------------------
# Generate Plan
# ---------------------------------------------------

if generate:

    if not activities:

        st.warning("Please choose at least one activity.")

    else:

        planner_request = PlannerRequest(
            activities=activities,
            preferred_time=preferred_time,
            objective=objective,
            heat_sensitive=heat_sensitive,
            cold_sensitive=cold_sensitive,
            rain_sensitive=rain_sensitive,
            long_commute=long_commute,
        )

        with st.spinner("Generating your personalized plan..."):

            plan = generate_daily_plan(
                weather,
                planner_request,
            )

            st.session_state.planner_output = plan

# ---------------------------------------------------
# Results
# ---------------------------------------------------

plan = st.session_state.planner_output

if plan is None:
    st.info("Generate a plan to see recommendations.")
    st.stop()

st.success("Plan Generated Successfully")

# ---------------------------------------------------
# Summary
# ---------------------------------------------------

st.subheader("📝 Daily Summary")

st.write(plan.summary)

st.divider()

# ---------------------------------------------------
# Activity Recommendations
# ---------------------------------------------------

st.subheader("🎯 Activity Recommendations")

activity_rows = []

for activity in plan.activities:

    activity_rows.append(
        {
            "Activity": activity.activity,
            "Score (/10)": activity.score,
            "Decision": activity.decision,
            "Reason": activity.reason,
        }
    )

st.dataframe(
    activity_rows,
    use_container_width=True,
    hide_index=True,
)

st.divider()

# ---------------------------------------------------
# Timeline
# ---------------------------------------------------

st.subheader("🕒 Suggested Timeline")

for item in plan.timeline:

    with st.container():

        col1, col2 = st.columns([1, 5])

        col1.markdown(f"### {item.time}")

        col2.write(item.recommendation)

st.divider()

# ---------------------------------------------------
# Packing List
# ---------------------------------------------------

st.subheader("🎒 Packing Checklist")

for item in plan.packing_list:

    st.checkbox(
        item,
        value=True,
        disabled=True,
    )

st.divider()

# ---------------------------------------------------
# Warnings
# ---------------------------------------------------

st.subheader("⚠ Weather Alerts")

if plan.warnings:

    for warning in plan.warnings:

        st.warning(warning)

else:

    st.success("No significant weather warnings.")