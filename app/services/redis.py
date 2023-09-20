from redis import asyncio as aioredis

from app.core.config import settings

rd = aioredis.Redis(host=settings.redis_host, port=settings.redis_port)
