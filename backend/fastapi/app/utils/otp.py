import random
import string
from .redis import RedisService

redis_service = RedisService()

def generate_random_otp(length: int = 6) -> str:
    return ''.join(random.choices(string.digits, k=length))

async def generate_otp(identifier: str, ttl: int = 300) -> str:
    otp = generate_random_otp()
    await redis_service.set(f"otp:{identifier}", otp, ttl)
    return otp

async def verify_otp(identifier: str, otp: str) -> bool:
    cached_otp = await redis_service.get(f"otp:{identifier}")
    if cached_otp and cached_otp == otp:
        return True
    return False

async def evict_otp(identifier: str) -> None:
    await redis_service.delete(f"otp:{identifier}")
