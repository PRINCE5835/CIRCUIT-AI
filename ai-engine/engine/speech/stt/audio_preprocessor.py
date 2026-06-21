"""
Audio preprocessor — resamples, normalizes, and formats audio
before STT inference. Supports file paths and raw bytes.
"""
import io
import wave
import numpy as np
from typing import Optional
from ...core.config import settings


class AudioPreprocessor:
    def __init__(self, sample_rate: int = settings.audio_sample_rate):
        self.target_rate = sample_rate

    def resample(self, audio: np.ndarray, orig_rate: int) -> np.ndarray:
        if orig_rate == self.target_rate:
            return audio
        ratio = self.target_rate / orig_rate
        new_len = int(len(audio) * ratio)
        return np.interp(
            np.linspace(0, len(audio) - 1, new_len),
            np.arange(len(audio)),
            audio,
        )

    def normalize(self, audio: np.ndarray) -> np.ndarray:
        peak = np.max(np.abs(audio))
        if peak > 0:
            return audio / peak
        return audio

    def to_mono(self, audio: np.ndarray) -> np.ndarray:
        if audio.ndim > 1:
            return np.mean(audio, axis=1)
        return audio

    def to_int16(self, audio: np.ndarray) -> np.ndarray:
        return (audio * 32767).astype(np.int16)

    def from_wav_bytes(self, wav_bytes: bytes) -> Optional[np.ndarray]:
        try:
            with io.BytesIO(wav_bytes) as buf:
                with wave.open(buf, "rb") as wf:
                    frames = wf.readframes(wf.getnframes())
                    dtype = np.int16 if wf.getsampwidth() == 2 else np.int8
                    audio = np.frombuffer(frames, dtype=dtype).astype(np.float32)
                    audio /= 32767.0 if wf.getsampwidth() == 2 else 127.0
                    rate = wf.getframerate()
            audio = self.to_mono(audio)
            audio = self.resample(audio, rate)
            audio = self.normalize(audio)
            return audio
        except Exception:
            return None

    def to_wav_bytes(self, audio: np.ndarray, sample_rate: Optional[int] = None) -> bytes:
        audio = self.to_int16(audio)
        rate = sample_rate or self.target_rate
        with io.BytesIO() as buf:
            with wave.open(buf, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(rate)
                wf.writeframes(audio.tobytes())
            return buf.getvalue()


preprocessor = AudioPreprocessor()
