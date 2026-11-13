from unittest.mock import patch

from llm.client import LLMError
from services.cache import TTLCache
from services.summarizer import FALLBACK_RESPONSE, Summarizer


class DummyCache:
    def __init__(self):
        self._store = {}

    def get(self, text: str) -> str | None:
        return self._store.get(text)

    def set(self, text: str, value: str) -> None:
        self._store[text] = value


def test_summarizer_success():
    with patch("services.summarizer.call_llm", return_value="Краткий пересказ текста."):
        s = Summarizer()
        result = s.process("Какой-то длинный текст для проверки.")
        assert result["summary"] == "Краткий пересказ текста."
        assert result["cached"] is False
        assert result["model"] != "fallback"


def test_summarizer_fallback():
    with patch("services.summarizer.call_llm", side_effect=LLMError("test error")):
        s = Summarizer()
        result = s.process("Какой-то текст.")
        assert result["summary"] == FALLBACK_RESPONSE
        assert result["model"] == "fallback"
        assert result["cached"] is False


def test_summarizer_cache_hit():
    dummy = DummyCache()
    dummy._store["Какой-то текст."] = "Закешированный ответ."
    with patch("services.summarizer.call_llm", return_value="Новый ответ."):
        s = Summarizer(cache=dummy)
        result = s.process("Какой-то текст.")
        assert result["summary"] == "Закешированный ответ."
        assert result["cached"] is True


def test_summarizer_cache_miss():
    dummy = DummyCache()
    with patch("services.summarizer.call_llm", return_value="Новый ответ."):
        s = Summarizer(cache=dummy)
        result = s.process("Новый текст.")
        assert result["summary"] == "Новый ответ."
        assert result["cached"] is False
        assert dummy._store.get("Новый текст.") == "Новый ответ."


def test_cache_ttl():
    cache = TTLCache(ttl=0)
    cache.set("text", "value")
    import time
    time.sleep(0.01)
    assert cache.get("text") is None
