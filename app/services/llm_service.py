from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

LLM_ENABLED = os.getenv("LLM_ENABLED", "true").lower() in {
    "1",
    "true",
    "yes",
    "on",
}


def get_llm(model: str = "gemini-2.0-flash", temperature: float = 0):
    if not LLM_ENABLED:
        return None
    return ChatGoogleGenerativeAI(
        model=model, temperature=temperature, google_api_key=os.getenv("GOOGLE_API_KEY")
    )
