import redis
import json
import os
from typing import Optional
from app.schemas.summary_schema import Summary
from dotenv import load_dotenv

load_dotenv()


class HolidayCacheService:
    def __init__(self):
        self.redis = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=os.getenv("REDIS_PORT"),
            decode_responses=True,
            username=os.getenv("REDIS_USERNAME", "default"),
            password=os.getenv("REDIS_PASSWORD", "default"),
        )

    def _build_key(self, local_name: str, country: str) -> str:
        return f"holiday:{country}:{local_name}"

    def get(self, local_name: str, country: str) -> Optional[Summary]:
        key = self._build_key(local_name, country)
        cached = self.redis.get(key)

        if cached:
            return Summary(**json.loads(cached))
        return None

    def set(self, holiday_summary: Summary, holiday_country: str, ttl: int = 86400):
        key = self._build_key(holiday_summary.name, holiday_country)
        self.redis.set(key, holiday_summary.model_dump_json(), ex=ttl)
