import logging

from config.settings import settings
from llm.client import LLMError, call_llm
from llm.prompts import build_prompt
from services.cache import TTLCache

logger = logging.getLogger(__name__)

FALLBACK_RESPONSE = "⚠️ Сервис временно недоступен. Пожалуйста, попробуйте позже."


class Summarizer:
    def __init__(self, cache: TTLCache | None = None):
        self._cache = cache

    def process(self, text: str) -> dict:
        logger.info("Processing request, text length=%d", len(text))

        if self._cache:
            cached = self._cache.get(text)
            if cached is not None:
                logger.info("Cache hit, returning cached result")
                return {
                    "summary": cached,
                    "model": settings.llm_model,
                    "cached": True,
                }
            logger.info("Cache miss, will call LLM")

        messages = build_prompt(text)
        logger.debug("Prompt built: %s", messages)

        try:
            response_text = call_llm(messages)
        except LLMError as e:
            logger.error("LLM call failed: %s", e)
            response_text = FALLBACK_RESPONSE

        cleaned = self._post_process(response_text)
        logger.info("Response ready, length=%d", len(cleaned))

        if self._cache and cleaned != FALLBACK_RESPONSE:
            self._cache.set(text, cleaned)

        return {
            "summary": cleaned,
            "model": settings.llm_model if cleaned != FALLBACK_RESPONSE else "fallback",
            "cached": False,
        }

    def _post_process(self, text: str) -> str:
        text = text.strip()
        return text
