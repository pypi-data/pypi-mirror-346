from pydantic_settings import BaseSettings


class StateManagerSettings(BaseSettings):
    REDIS_URL: str = "redis://localhost:6379/0"


state_manager_settings = StateManagerSettings()
