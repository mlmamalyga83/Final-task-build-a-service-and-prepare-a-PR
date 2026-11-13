import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routes import init_routes, router
from config.settings import settings
from services.cache import TTLCache
from services.summarizer import Summarizer

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting LLM Summarizer service")
    cache = TTLCache()
    summarizer = Summarizer(cache=cache)
    init_routes(summarizer)
    logger.info("Service initialized, model=%s, cache_ttl=%ds", settings.llm_model, settings.cache_ttl)
    yield
    logger.info("Shutting down LLM Summarizer service")


app = FastAPI(title="LLM Summarizer", version="1.0.0", lifespan=lifespan)
app.include_router(router)
