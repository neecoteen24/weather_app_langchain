import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from utils.logger import logger

load_dotenv()


def get_llm() -> ChatGoogleGenerativeAI:
    """
    Create and return a configured Gemini LLM instance.
    """

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        logger.error("GOOGLE_API_KEY not found in environment variables")
        raise ValueError(
            "GOOGLE_API_KEY not found in environment variables."
        )

    logger.info("Creating Gemini LLM client")

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        google_api_key=api_key,
    )