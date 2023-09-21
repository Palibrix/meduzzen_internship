import redis
from redis import asyncio as aioredis

from app.core.config import settings


pool = redis.ConnectionPool(
	host=settings.redis_host,
	port=settings.redis_port
)


def get_redis():
	return aioredis.Redis(connection_pool=pool)
