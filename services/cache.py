import hashlib
import logging
import time

from config.settings import settings

logger = logging.getLogger(__name__)


class TTLCache:
    def __init__(self, ttl: int | None = None):
        self._ttl = settings.cache_ttl if ttl is None else ttl
        self._store: dict[str, tuple[str, float]] = {}

    def _make_key(self, text: str) -> str:
        return hashlib.sha256(f"summarize:{text}".encode()).hexdigest()

    def get(self, text: str) -> str | None:
        key = self._make_key(text)
        entry = self._store.get(key)
        if entry is None:
            logger.debug("Cache miss for key=%s", key[:16])
            return None
        value, expires_at = entry
        if time.time() > expires_at:
            logger.debug("Cache expired for key=%s", key[:16])
            del self._store[key]
            return None
        logger.debug("Cache hit for key=%s", key[:16])
        return value

    def set(self, text: str, value: str) -> None:
        key = self._make_key(text)
        expires_at = time.time() + self._ttl
        self._store[key] = (value, expires_at)
        logger.debug("Cache set for key=%s, ttl=%ds", key[:16], self._ttl)

    def clear(self) -> None:
        self._store.clear()
