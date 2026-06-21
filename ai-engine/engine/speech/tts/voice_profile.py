from dataclasses import dataclass


@dataclass
class VoiceProfile:
    name: str
    piper_model: str
    locale: str
    speed: float = 1.0
    pitch: float = 1.0
    description: str = ""
    sample_rate: int = 22050


VOICE_PROFILES: dict[str, VoiceProfile] = {
    "en-male": VoiceProfile(
        name="English (Male)",
        piper_model="en_US-lessac-medium",
        locale="en_US",
        speed=1.0,
        description="Clear male English voice",
    ),
    "en-female": VoiceProfile(
        name="English (Female)",
        piper_model="en_US-amy-medium",
        locale="en_US",
        speed=1.0,
        description="Warm female English voice",
    ),
    "en-low": VoiceProfile(
        name="English (Lightweight)",
        piper_model="en_US-lessac-low",
        locale="en_US",
        speed=1.0,
        description="Low-resource English TTS",
    ),
    "hi-male": VoiceProfile(
        name="Hindi (Male)",
        piper_model="hi_IN-male-medium",
        locale="hi_IN",
        speed=1.0,
        description="Hindi male voice",
    ),
    "hi-female": VoiceProfile(
        name="Hindi (Female)",
        piper_model="hi_IN-female-medium",
        locale="hi_IN",
        speed=1.0,
        description="Hindi female voice",
    ),
}


def get_profile(name: str = "en-male") -> VoiceProfile:
    return VOICE_PROFILES.get(name, VOICE_PROFILES["en-male"])
