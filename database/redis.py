from redis.asyncio import Redis
from ml_fastapi.config import settings


_blacklisted_tokens = Redis(host=settings.redis_host,
 port=settings.redis_port,
  db=0)

async def add_jti_to_blackist(jti: str):
    """Adds a JWT token ID to the blacklist."""
    return await _blacklisted_tokens.set(jti, "blacklisted")

async def is_token_blacklisted(jti: str)->bool:
    """Checks if a JWT token ID is in the blacklist."""
    return bool(await _blacklisted_tokens.exists(jti))
