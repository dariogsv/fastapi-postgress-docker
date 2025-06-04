# Exemplo de app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str
    
    # Para carregar do .env automaticamente
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')


settings = Settings()