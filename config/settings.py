
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    llm_api_key: str = ""
    llm_model: str = "gpt-3.5-turbo"
    llm_timeout: int = 30
    llm_max_tokens: int = 500
    llm_temperature: float = 0.7
    llm_base_url: str = "https://api.openai.com/v1"

    cache_ttl: int = 3600

    log_level: str = "INFO"


settings = Settings()