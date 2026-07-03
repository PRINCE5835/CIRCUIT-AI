from pathlib import Path

from pydantic_settings import BaseSettings

_ENGINE_DIR = Path(__file__).resolve().parent.parent.parent


def _abs(path: str) -> str:
    return str(_ENGINE_DIR / path)


class Settings(BaseSettings):
    app_name: str = "BreadBoard AI Engine"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True  # Overridden by ENVIRONMENT: debug = (environment == "development")

    @property
    def is_debug(self) -> bool:
        return self.environment == "development"

    host: str = "0.0.0.0"
    port: int = 8001

    # ── Ollama ──────────────────────────────────────────────
    ollama_host: str = "http://localhost:11434"
    ollama_request_timeout: int = 120

    # Primary model for circuit generation & reasoning (text-only)
    ollama_primary_model: str = "qwen2.5:1.5b"
    # Vision model (must support image input — e.g., llava, llama3.2-vision)
    ollama_vision_model: str = "llava"
    # Coding-specific model
    ollama_coder_model: str = "qwen2.5:1.5b"
    # Lightweight model for simple tasks
    ollama_light_model: str = "qwen2.5:1.5b"

    # ── Speech-to-Text ──────────────────────────────────────
    whisper_model_size: str = "base"
    whisper_model_path: str = _abs("engine/models/whisper/")
    vosk_model_path: str = _abs("engine/models/vosk/")
    vosk_model_lang: str = "en"
    audio_sample_rate: int = 16000
    audio_channels: int = 1

    # ── Text-to-Speech (Piper) ─────────────────────────────
    piper_binary_path: str = "/usr/local/bin/piper"
    piper_model_path: str = _abs("engine/models/piper/")
    piper_default_voice: str = "en_US-lessac-medium"
    piper_output_sample_rate: int = 22050

    # ── Vision ──────────────────────────────────────────────
    yolo_model_path: str = _abs("engine/models/yolo/")
    yolo_model_name: str = "best.pt"
    yolo_confidence_threshold: float = 0.4
    yolo_iou_threshold: float = 0.45
    ocr_model_path: str = _abs("engine/models/ocr/")

    # ── CORS ────────────────────────────────────────────────
    backend_cors_origins: str = "http://localhost:8000,http://localhost:8080"

    # ── Circuit ──────────────────────────────────────────────
    max_netlist_length: int = 50000
    circuit_safety_timeout: int = 30

    model_config = {"env_file": ".env", "case_sensitive": False}


settings = Settings()
