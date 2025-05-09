from pydantic_settings import BaseSettings


class StateManagerSettings(BaseSettings):
    STATE_MANAGER_REDIS_URL: str = "redis://localhost:6379/0"


state_manager_settings = StateManagerSettings()
