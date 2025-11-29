"""
LLM module for Groq integration with DeepSeek R1 model.
All LLM calls go through this module.
"""
from langchain_groq import ChatGroq
from rag_app.config import GROQ_API_KEY, DEFAULT_MODEL, LLM_TEMPERATURE


def get_llm(
    model: str = DEFAULT_MODEL,
    temperature: float = LLM_TEMPERATURE,
    **kwargs
) -> ChatGroq:
    """
    Factory function to get the configured Groq LLM.

    Args:
        model: Model identifier (default: deepseek-r1-distill-llama-70b)
        temperature: Temperature for generation (default: 0.0 for stability)
        **kwargs: Additional arguments to pass to ChatGroq

    Returns:
        ChatGroq instance configured with DeepSeek R1

    Raises:
        ValueError: If GROQ_API_KEY is not set
    """
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is not set. Please check your .env file."
        )

    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=model,
        temperature=temperature,
        **kwargs
    )
