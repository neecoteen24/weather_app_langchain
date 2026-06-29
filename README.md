# AI Weather Assistant

A small Streamlit app that lets you enter a city and get the current weather plus AI-generated recommendations for clothing, outdoor activity, and safety precautions.

## Features

- Fetches live weather data from WeatherAPI
- Uses Google Gemini via LangChain to generate concise weather-based advice
- Shows key weather metrics in a simple Streamlit dashboard

## Requirements

- Python 3.10 or newer
- A WeatherAPI account and API key
- A Google Generative AI key for Gemini

## Setup

1. Create and activate a virtual environment.
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your API keys:

```env
WEATHER_API_KEY=your_weatherapi_key
GOOGLE_API_KEY=your_google_gemini_key
```

## Run the app

Start the Streamlit app with:

```bash
streamlit run app.py
```

Then enter a city name in the browser UI and click **Get Weather**.

## How it works

- `weather.py` reads `WEATHER_API_KEY`, calls WeatherAPI, and normalizes the response.
- `chains.py` loads the Gemini model and generates the recommendation text.
- `app.py` renders the Streamlit interface and displays the weather summary and recommendations.

## Troubleshooting

- If weather lookup fails, confirm that `WEATHER_API_KEY` is set correctly in `.env`.
- If recommendations fail, confirm that your Google Generative AI credentials are configured for LangChain.
- If Streamlit does not start, make sure the virtual environment is active and dependencies are installed.