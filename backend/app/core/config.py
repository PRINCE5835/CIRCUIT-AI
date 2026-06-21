from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "BreadBoard AI"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    backend_secret_key: str = "change-me-to-a-random-secret"
    backend_cors_origins: str = "*"
    backend_rate_limit: str = "100/minute"

    database_url: str = "mysql+aiomysql://breadboard:breadboard@localhost:3306/breadboard"

    ai_engine_host: str = "127.0.0.1"
    ai_engine_port: int = 8001
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llava"
    ollama_timeout: int = 120

    whisper_model_size: str = "base"
    vosk_model_path: str = "./engine/models/vosk/"

    yolo_model_path: str = "./engine/models/yolo/"
    ocr_model_path: str = "./engine/models/ocr/"

    jwt_secret_key: str = "change-me-to-a-random-jwt-secret"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    redis_url: str = "redis://localhost:6379/0"
    cache_ttl: int = 300

    sentry_dsn: str = ""
    prometheus_enabled: bool = False

    model_config = {"env_file": ".env", "case_sensitive": False, "extra": "ignore"}


settings = Settings()
