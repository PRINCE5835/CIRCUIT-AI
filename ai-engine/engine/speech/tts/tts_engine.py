"""
Piper TTS Engine — runs Piper locally as a subprocess
for fast offline text-to-speech on CPU.
"""
import io
import subprocess
import logging
import numpy as np
from pathlib import Path
from typing import Optional
from .voice_profile import VoiceProfile, get_profile
from engine.core.config import settings

logger = logging.getLogger(__name__)


class PiperTTS:
    def __init__(self, binary: str = settings.piper_binary_path):
        self._binary = Path(binary)
        self._available = self._binary.exists()

    def _model_file(self, profile: VoiceProfile, ext: str = ".onnx") -> Path:
        return Path(settings.piper_model_path) / f"{profile.piper_model}{ext}"

    def is_available(self) -> bool:
        return self._available

    async def check_voice(self, profile: VoiceProfile) -> bool:
        model = self._model_file(profile)
        config = self._model_file(profile, ".json")
        return model.exists() and config.exists()

    async def synthesize(
        self,
        text: str,
        voice: str = settings.piper_default_voice,
        output_sample_rate: int = settings.piper_output_sample_rate,
    ) -> Optional[bytes]:
        """Synthesize text to 16-bit PCM WAV bytes."""
        if not self._available:
            logger.warning("Piper binary not found at %s", self._binary)
            return None

        profile = get_profile(voice)
        model_path = self._model_file(profile)
        if not model_path.exists():
            logger.warning("Piper model not found at %s", model_path)
            return None

        try:
            proc = subprocess.Popen(
                [
                    str(self._binary),
                    "--model", str(model_path),
                    "--output-raw",
                    "--length-scale", str(profile.speed),
                    "--sample-rate", str(output_sample_rate),
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            raw_audio, stderr = proc.communicate(
                input=text.encode("utf-8"),
                timeout=30,
            )

            if proc.returncode != 0:
                logger.error("Piper failed: %s", stderr.decode())
                return None

            audio_array = np.frombuffer(raw_audio, dtype=np.int16)
            return self._raw_to_wav(audio_array, output_sample_rate)

        except subprocess.TimeoutExpired:
            proc.kill()
            logger.error("Piper timed out")
            return None
        except FileNotFoundError:
            self._available = False
            logger.error("Piper binary not found")
            return None

    def _raw_to_wav(self, audio: np.ndarray, sample_rate: int) -> bytes:
        import wave
        with io.BytesIO() as buf:
            with wave.open(buf, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(audio.tobytes())
            return buf.getvalue()

    async def list_available_models(self) -> list[str]:
        from .voice_profile import VOICE_PROFILES
        available = []
        for name, profile in VOICE_PROFILES.items():
            if await self.check_voice(profile):
                available.append(name)
        return available


# Singleton
tts = PiperTTS()
