import json
import logging
import numpy as np
from pathlib import Path
from .audio_preprocessor import preprocessor
from ...core.config import settings

logger = logging.getLogger(__name__)


class VoskHandler:
    def __init__(self, model_path: str = settings.vosk_model_path):
        self.model_path = Path(model_path)
        self._model = None
        self._available = False

    async def load(self, lang: str = settings.vosk_model_lang) -> bool:
        try:
            from vosk import Model, SetLogLevel
            SetLogLevel(-1)

            if lang == "hi":
                folders = [f for f in self.model_path.iterdir() if f.is_dir()]

                if not folders:
                    raise Exception("No Vosk model folder found")

                model_dir = folders[0]

            else:
                folders = [f for f in self.model_path.iterdir() if f.is_dir()]

                if not folders:
                    raise Exception("No Vosk model folder found")

                model_dir = folders[0]

            if not model_dir.exists():
                logger.warning("Vosk model not found at %s", model_dir)
                self._available = False
                return False

            self._model = Model(str(model_dir))
            self._available = True
            logger.info("Vosk %s model loaded", lang)
            return True
        except Exception as e:
            logger.warning("Failed to load Vosk: %s", e)
            self._available = False
            return False

    async def transcribe(self, audio: np.ndarray) -> dict[str, str]:
        if not self._model or not self._available:
            return {"text": "", "error": "Vosk model not loaded"}

        from vosk import KaldiRecognizer
        rec = KaldiRecognizer(self._model, settings.audio_sample_rate)

        audio_int16 = preprocessor.to_int16(audio)
        if rec.AcceptWaveform(audio_int16.tobytes()):
            result = json.loads(rec.Result())
        else:
            result = json.loads(rec.FinalResult())

        return {
            "text": result.get("text", "").strip(),
            "partial": result.get("partial", ""),
        }

    async def transcribe_bytes(self, wav_bytes: bytes) -> dict[str, str]:
        audio = preprocessor.from_wav_bytes(wav_bytes)
        if audio is None:
            return {"text": "", "error": "Invalid WAV data"}
        return await self.transcribe(audio)

    def unload(self):
        self._model = None
        self._available = False


handler = VoskHandler()
