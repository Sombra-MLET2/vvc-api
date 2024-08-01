import logging

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

logger = logging.getLogger(__name__)


async def cache_startup():
    logger.info("Starting cache in-memory backend")
    FastAPICache.init(InMemoryBackend(), prefix="api-cache")
