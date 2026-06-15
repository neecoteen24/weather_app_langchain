from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3
)

recommendation_prompt = ChatPromptTemplate.from_template(
"""
Based on the current weather conditions:

Temperature : {temperature} °C
Humidity : {humidity} %
Wind Speed : {wind_speed} km/h
Condition : {condition}

Give:

1. Clothing recommendation
2. Outdoor activity recommendation
3. Safety precautions

Keep it concise.
"""
)

recommendation_chain = recommendation_prompt | llm


def run_weather_chains(weather_data):

    recommendation = recommendation_chain.invoke(
        weather_data
    ).content

    return {
        "recommendation": recommendation
    }