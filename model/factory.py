from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from config.config import (
    ANTHROPIC_API_KEY,
    DEFAULT_MODEL,
    GEMINI_API_KEY,
    LLM_PROVIDER,
    OPENAI_API_KEY,
)


def get_chat_model():
    """Devuelve el chat model de LangChain según LLM_PROVIDER."""
    provider = (LLM_PROVIDER or "gemini").strip().lower()

    if provider == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no está configurada")
        return ChatOpenAI(model=DEFAULT_MODEL, api_key=OPENAI_API_KEY)

    if provider == "gemini":
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY no está configurada")
        return ChatGoogleGenerativeAI(model=DEFAULT_MODEL, google_api_key=GEMINI_API_KEY)

    if provider == "anthropic":
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY no está configurada")
        return ChatAnthropic(model=DEFAULT_MODEL, api_key=ANTHROPIC_API_KEY)

    raise ValueError(
        f"Proveedor no soportado: '{provider}'. "
        "Usa uno de: openai, gemini, anthropic"
    )
