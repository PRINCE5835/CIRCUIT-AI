"""
Model registry — manages available local models and their lifecycle.
Tracks which models are downloaded, their paths, and capabilities.
"""
# flake8: noqa: E501
import os
from enum import Enum
from dataclasses import dataclass
from typing import Optional

from .config import settings


class ModelCapability(str, Enum):
    TEXT_GENERATION = "text_generation"
    CODE_GENERATION = "code_generation"
    REASONING = "reasoning"
    SPEECH_TO_TEXT = "speech_to_text"
    TEXT_TO_SPEECH = "text_to_speech"
    VISION = "vision"
    EMBEDDING = "embedding"


class ModelProvider(str, Enum):
    OLLAMA = "ollama"
    WHISPER = "whisper"
    VOSK = "vosk"
    PIPER = "piper"


@dataclass
class ModelInfo:
    name: str
    provider: ModelProvider
    capability: list[ModelCapability]
    path: Optional[str] = None
    size_mb: int = 0
    is_downloaded: bool = False
    ollama_tag: Optional[str] = None  # e.g. "qwen3"
    description: str = ""

    def full_path(self) -> Optional[str]:
        if self.path and os.path.exists(self.path):
            return self.path
        return None


# ── Registry ──────────────────────────────────────────────────

MODEL_REGISTRY: dict[str, ModelInfo] = {
    # ── Ollama Models ──────────────────────────────────────────
    "llava": ModelInfo(
        name="LLaVA 7B",
        provider=ModelProvider.OLLAMA,
        capability=[ModelCapability.TEXT_GENERATION, ModelCapability.REASONING, ModelCapability.VISION],
        ollama_tag="llava",
        size_mb=4500,
        description="Primary vision & reasoning model",
    ),
    "deepseek-coder:6.7b": ModelInfo(
        name="DeepSeek Coder 6.7B",
        provider=ModelProvider.OLLAMA,
        capability=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
        ollama_tag="deepseek-coder:6.7b",
        size_mb=3800,
        description="Code generation & netlist parsing",
    ),
    "deepseek-coder:1.3b": ModelInfo(
        name="DeepSeek Coder 1.3B",
        provider=ModelProvider.OLLAMA,
        capability=[ModelCapability.CODE_GENERATION],
        ollama_tag="deepseek-coder:1.3b",
        size_mb=800,
        description="Lightweight code model for simple generation",
    ),
    "gemma3:12b": ModelInfo(
        name="Gemma 3 12B",
        provider=ModelProvider.OLLAMA,
        capability=[ModelCapability.TEXT_GENERATION, ModelCapability.REASONING],
        ollama_tag="gemma3:12b",
        size_mb=7200,
        description="High-quality instruction following",
    ),
    "gemma3:2b": ModelInfo(
        name="Gemma 3 2B",
        provider=ModelProvider.OLLAMA,
        capability=[ModelCapability.TEXT_GENERATION],
        ollama_tag="gemma3:2b",
        size_mb=1200,
        description="Fast lightweight model for simple Q&A",
    ),

    # ── Whisper Models ─────────────────────────────────────────
    "whisper-tiny": ModelInfo(
        name="Whisper Tiny",
        provider=ModelProvider.WHISPER,
        capability=[ModelCapability.SPEECH_TO_TEXT],
        path=settings.whisper_model_path + "tiny.pt",
        size_mb=150,
        description="Fastest STT, ~32x speed, 32M params",
    ),
    "whisper-base": ModelInfo(
        name="Whisper Base",
        provider=ModelProvider.WHISPER,
        capability=[ModelCapability.SPEECH_TO_TEXT],
        path=settings.whisper_model_path + "base.pt",
        size_mb=290,
        description="Balanced STT, ~16x speed, 74M params",
    ),
    "whisper-small": ModelInfo(
        name="Whisper Small",
        provider=ModelProvider.WHISPER,
        capability=[ModelCapability.SPEECH_TO_TEXT],
        path=settings.whisper_model_path + "small.pt",
        size_mb=970,
        description="Accurate STT, ~6x speed, 244M params",
    ),

    # ── Vosk Models ────────────────────────────────────────────
    "vosk-en": ModelInfo(
        name="Vosk English",
        provider=ModelProvider.VOSK,
        capability=[ModelCapability.SPEECH_TO_TEXT],
        path=settings.vosk_model_path + "vosk-model-en-us-0.42",
        size_mb=180,
        description="Offline English STT (low latency)",
    ),
    "vosk-hi": ModelInfo(
        name="Vosk Hindi",
        provider=ModelProvider.VOSK,
        capability=[ModelCapability.SPEECH_TO_TEXT],
        path=settings.vosk_model_path + "vosk-model-hi-0.22",
        size_mb=160,
        description="Offline Hindi STT",
    ),

    # ── Piper TTS Models ───────────────────────────────────────
    "piper-en": ModelInfo(
        name="Piper English (Lessac)",
        provider=ModelProvider.PIPER,
        capability=[ModelCapability.TEXT_TO_SPEECH],
        path=settings.piper_model_path + "en_US-lessac-medium",
        size_mb=110,
        description="English TTS voice",
    ),
    "piper-en-low": ModelInfo(
        name="Piper English Low",
        provider=ModelProvider.PIPER,
        capability=[ModelCapability.TEXT_TO_SPEECH],
        path=settings.piper_model_path + "en_US-lessac-low",
        size_mb=40,
        description="Lightweight English TTS",
    ),
}


class ModelRegistry:
    """Manages available model discovery and lifecycle."""

    def __init__(self):
        self._models = dict(MODEL_REGISTRY)
        self._refresh_downloaded_status()

    def _refresh_downloaded_status(self):
        for name, model in self._models.items():
            if model.provider == ModelProvider.OLLAMA:
                model.is_downloaded = True  # Ollama manages this externally
            elif model.path:
                model.is_downloaded = os.path.exists(model.path)

    def get(self, name: str) -> Optional[ModelInfo]:
        return self._models.get(name)

    def list_available(self) -> list[ModelInfo]:
        return [m for m in self._models.values() if m.is_downloaded]

    def list_by_capability(self, capability: ModelCapability) -> list[ModelInfo]:
        return [
            m for m in self._models.values()
            if capability in m.capability and m.is_downloaded
        ]

    def list_by_provider(self, provider: ModelProvider) -> list[ModelInfo]:
        return [m for m in self._models.values() if m.provider == provider]

    def get_primary(self) -> ModelInfo:
        return self._models.get(settings.ollama_primary_model, self._models["llava"])

    def get_coder(self) -> ModelInfo:
        return self._models.get(settings.ollama_coder_model, self._models["deepseek-coder:6.7b"])

    def get_light(self) -> ModelInfo:
        return self._models.get(settings.ollama_light_model, self._models["gemma3:2b"])

    def get_default_stt(self) -> ModelInfo:
        return self._models.get("whisper-base", self._models["whisper-tiny"])

    def get_default_tts(self) -> ModelInfo:
        return self._models.get("piper-en", self._models["piper-en-low"])


registry = ModelRegistry()
