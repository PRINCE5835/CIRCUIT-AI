"""Query classifier — categorises user queries into intent types for routing."""

from typing import Literal

QueryType = Literal[
    "circuit_generation",
    "repair",
    "verification",
    "learning",
    "marketplace",
    "general",
]

CATEGORY_KEYWORDS: dict[QueryType, list[str]] = {
    "circuit_generation": [
        "build", "make", "create", "design", "construct", "circuit for",
        "schematic", "circuit diagram", "how to make", "how to build",
        "how to create", "wiring", "breadboard layout", "circuit idea",
        "project", "blink", "led", "buzzer", "battery tester",
        "push button", "darkness detector", "light sensor",
        "transistor switch", "water level indicator", "rain alarm",
        "touch sensor", "clap switch", "burglar alarm", "fire alarm",
        "smoke detector", "doorbell", "mini fan", "temperature alarm",
        "motion detector", "gas leakage", "ir sensor", "ultrasonic sensor",
        "ldr", "pir", "flame sensor", "humidity sensor", "soil moisture",
        "sound sensor", "voltage regulator", "relay", "traffic light",
        "digital counter", "frequency generator", "555 timer",
        "led chaser", "police light", "emergency light",
        "mobile charger", "battery charging", "power supply",
        "arduino led", "arduino traffic", "arduino temperature",
        "arduino ultrasonic", "arduino smart light",
        "bluetooth controlled", "smart irrigation", "home automation",
        "smart parking", "beginner electronics project",
    ],
    "repair": [
        "repair", "fix", "broken", "not working", "fault", "issue",
        "problem", "troubleshoot", "diagnose", "why isn't",
        "why is my", "dead", "no power", "shorts", "burn",
        "overheat", "smoke", "replace component",
    ],
    "verification": [
        "verify", "check if", "is this correct", "validate",
        "does this look right", "review my circuit", "am i right",
        "is my circuit", "correct me", "what's wrong with",
        "double check", "confirm",
    ],
    "learning": [
        "what is", "explain", "how does", "how do", "teach me",
        "learn", "tutorial", "guide", "understand", "basics of",
        "introduction to", "what are", "what does", "difference between",
        "compare", "working of", "principle", "how it works",
        "what does a", "what does an",
    ],
    "marketplace": [
        "buy", "price", "cost", "shop", "purchase", "where to get",
        "how much", "cheap", "affordable", "seller", "marketplace",
        "available", "order", "delivery", "component price",
    ],
}


def classify(query: str) -> QueryType:
    q = query.lower().strip()

    for qtype, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in q:
                return qtype

    return "general"


def is_electronics_query(query: str) -> bool:
    return classify(query) != "general"
