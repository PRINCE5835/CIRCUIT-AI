from dataclasses import dataclass
from enum import Enum


class ModelProvider(str, Enum):
    OLLAMA = "ollama"


@dataclass
class ModelInfo:
    name: str
    provider: ModelProvider = ModelProvider.OLLAMA
    ollama_tag: str | None = None
