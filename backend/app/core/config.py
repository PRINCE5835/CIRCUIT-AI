from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    app_name: str = "BreadBoard AI"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = False
    log_level: str = "INFO"

    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    backend_secret_key: str = ""
    backend_cors_origins: str = "http://localhost:8080,http://localhost:5000"
    backend_rate_limit: str = "100/minute"

    database_url: str = "postgresql+asyncpg://breadboard:breadboard@localhost:5432/breadboard"

    ai_engine_host: str = "127.0.0.1"
    ai_engine_port: int = 8001
    ollama_host: str = "http://localhost:11434"
    circuit_ollama_host: str = ""
    ollama_api_key: str = ""
    ollama_model: str = "llama3.2:3b"
    ollama_vision_model: str = "llava"
    ollama_timeout: int = 120

    whisper_model_size: str = "base"
    vosk_model_path: str = "./engine/models/vosk/"

    yolo_model_path: str = "./engine/models/yolo/"
    ocr_model_path: str = "./engine/models/ocr/"

    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    redis_url: str = "redis://localhost:6379/0"
    cache_ttl: int = 300

    sentry_dsn: str = ""
    prometheus_enabled: bool = False

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore",
        "env_file_encoding": "utf-8",
    }

    @field_validator("database_url")
    @classmethod
    def fix_async_driver(cls, v: str) -> str:
        if v.startswith("postgresql://") and "+asyncpg" not in v:
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        if v.startswith("mysql://") and "+aiomysql" not in v:
            return v.replace("mysql://", "mysql+aiomysql://", 1)
        return v

    @field_validator("backend_secret_key", "jwt_secret_key")
    @classmethod
    def validate_secrets(cls, v: str) -> str:
        if not v:
            raise ValueError("Secret key must be set to a secure random value")
        if v in ("change-me", "REPLACE_WITH_SECURE_RANDOM_64_HEX_CHARS"):
            raise ValueError(
                "Secret key must be set to a secure random value. "
                "Generate one with: openssl rand -hex 32"
            )
        return v


settings = Settings()
