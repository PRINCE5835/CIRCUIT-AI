"""
Whisper STT handler — local inference via OpenAI Whisper.
Falls back gracefully if model not downloaded.
"""
# flake8: noqa: E501

import logging
from typing import Optional
import numpy as np
from .audio_preprocessor import preprocessor
from ...core.config import settings

logger = logging.getLogger(__name__)


class WhisperHandler:
    def __init__(self, model_size: str = settings.whisper_model_size):
        self.model_size = model_size
        self._model = None
        self._available = False

    async def load(self) -> bool:
        try:
            import whisper
            self._model = whisper.load_model(
                self.model_size,
                download_root=settings.whisper_model_path,
            )
            self._available = True
            logger.info("Whisper %s model loaded", self.model_size)
            return True
        except Exception as e:
            logger.warning("Failed to load Whisper: %s", e)
            self._available = False
            return False

    async def transcribe(
        self,
        audio: np.ndarray,
        language: Optional[str] = None,
        task: str = "transcribe",
    ) -> dict[str, str]:
        if not self._model or not self._available:
            return {"text": "", "error": "Whisper model not loaded"}

        audio = preprocessor.normalize(audio)
        result = self._model.transcribe(
            audio,
            language=language,
            task=task,
            fp16=False,
        )
        return {
            "text": result.get("text", "").strip(),
            "language": result.get("language", language or ""),
            "segments": result.get("segments", []),
        }

    async def transcribe_file(self, wav_path: str, language: Optional[str] = None) -> dict[str, str]:
        try:
            import librosa
            audio, _ = librosa.load(wav_path, sr=16000, mono=True)
            return await self.transcribe(audio, language)
        except Exception as e:
            return {"text": "", "error": str(e)}

    async def transcribe_bytes(self, wav_bytes: bytes, language: Optional[str] = None) -> dict[str, str]:
        audio = preprocessor.from_wav_bytes(wav_bytes)
        if audio is None:
            return {"text": "", "error": "Invalid WAV data"}
        return await self.transcribe(audio, language)

    def unload(self):
        self._model = None
        self._available = False


# Singleton, loaded on first use
handler = WhisperHandler()
