from redis import Redis
from src.config import state_manager_settings


redis_client = Redis.from_url(state_manager_settings.REDIS_URL)
