import logging

import httpx

from config.settings import settings

logger = logging.getLogger(__name__)


class LLMError(Exception):
    pass


def call_llm(messages: list[dict]) -> str:
    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.llm_model,
        "messages": messages,
        "max_tokens": settings.llm_max_tokens,
        "temperature": settings.llm_temperature,
    }

    try:
        with httpx.Client(timeout=settings.llm_timeout) as client:
            response = client.post(
                f"{settings.llm_base_url}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
    except httpx.TimeoutException:
        logger.error("LLM request timed out after %ds", settings.llm_timeout)
        raise LLMError("LLM request timed out")
    except httpx.RequestError as e:
        logger.error("LLM network error: %s", e)
        raise LLMError(f"LLM network error: {e}")
    except httpx.HTTPStatusError as e:
        logger.error("LLM returned HTTP %d: %s", e.response.status_code, e.response.text)
        raise LLMError(f"LLM returned HTTP {e.response.status_code}")

    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        logger.error("Unexpected LLM response format: %s", data)
        raise LLMError("Unexpected LLM response format")

    if not content or not content.strip():
        logger.warning("LLM returned empty content")
        raise LLMError("LLM returned empty content")

    return content.strip()
