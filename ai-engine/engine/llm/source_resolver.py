"""
Source Resolver — validates and caches priority source URLs.
Used by the AI Engine to verify sources before including them in LLM output.
"""
# flake8: noqa: E501
import json
import os
from typing import Optional
from dataclasses import dataclass

import httpx


@dataclass
class SourceEntry:
    title: str
    url: str
    source_type: str
    priority: int
    license: str = ""
    category: str = "general"

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "url": self.url,
            "source_type": self.source_type,
            "priority": self.priority,
            "license": self.license,
            "category": self.category,
        }


# ── Priority Source Registry ──────────────────────────────────
# These are manually curated, verified URLs from the priority sources.
# Order = priority (lower index = higher priority).

PRIORITY_SOURCES: list[SourceEntry] = [
    # ═══ WIKIPEDIA ═══ (priority 1)
    SourceEntry("Wikipedia - Ohm's Law", "https://en.wikipedia.org/wiki/Ohm%27s_law", "wikipedia", 1, "CC BY-SA 4.0"),
    SourceEntry("Wikipedia - Kirchhoff's Circuit Laws", "https://en.wikipedia.org/wiki/Kirchhoff%27s_circuit_laws", "wikipedia", 1, "CC BY-SA 4.0"),
    SourceEntry("Wikipedia - Resistor", "https://en.wikipedia.org/wiki/Resistor", "wikipedia", 1, "CC BY-SA 4.0"),
    SourceEntry("Wikipedia - Capacitor", "https://en.wikipedia.org/wiki/Capacitor", "wikipedia", 1, "CC BY-SA 4.0"),
    SourceEntry("Wikipedia - Inductor", "https://en.wikipedia.org/wiki/Inductor", "wikipedia", 1, "CC BY-SA 4.0"),
    SourceEntry("Wikipedia - Diode", "https://en.wikipedia.org/wiki/Diode", "wikipedia", 1, "CC BY-SA 4.0"),
    SourceEntry("Wikipedia - Transistor", "https://en.wikipedia.org/wiki/Transistor", "wikipedia", 1, "CC BY-SA 4.0"),
    SourceEntry("Wikipedia - Operational Amplifier", "https://en.wikipedia.org/wiki/Operational_amplifier", "wikipedia", 1, "CC BY-SA 4.0"),
    SourceEntry("Wikipedia - 555 Timer IC", "https://en.wikipedia.org/wiki/555_timer_IC", "wikipedia", 1, "CC BY-SA 4.0"),
    SourceEntry("Wikipedia - Arduino", "https://en.wikipedia.org/wiki/Arduino", "wikipedia", 1, "CC BY-SA 4.0"),
    SourceEntry("Wikipedia - Raspberry Pi", "https://en.wikipedia.org/wiki/Raspberry_Pi", "wikipedia", 1, "CC BY-SA 4.0"),
    SourceEntry("Wikipedia - Breadboard", "https://en.wikipedia.org/wiki/Breadboard", "wikipedia", 1, "CC BY-SA 4.0"),
    SourceEntry("Wikipedia - Printed Circuit Board", "https://en.wikipedia.org/wiki/Printed_circuit_board", "wikipedia", 1, "CC BY-SA 4.0"),
    SourceEntry("Wikipedia - Electronic Component", "https://en.wikipedia.org/wiki/Electronic_component", "wikipedia", 1, "CC BY-SA 4.0"),
    SourceEntry("Wikipedia - Series and Parallel Circuits", "https://en.wikipedia.org/wiki/Series_and_parallel_circuits", "wikipedia", 1, "CC BY-SA 4.0"),

    # ═══ ELECTRONICS TUTORIALS ═══ (priority 2)
    SourceEntry("Electronics Tutorials - Home", "https://www.electronics-tutorials.ws", "electronics_tutorials", 2, ""),
    SourceEntry("Electronics Tutorials - RC Networks", "https://www.electronics-tutorials.ws/rc/rc_1.html", "electronics_tutorials", 2, ""),
    SourceEntry("Electronics Tutorials - Op-amp Basics", "https://www.electronics-tutorials.ws/opamp/opamp_1.html", "electronics_tutorials", 2, ""),

    # ═══ ARDUINO DOCUMENTATION ═══ (priority 3)
    SourceEntry("Arduino - Getting Started", "https://docs.arduino.cc/learn/", "arduino_docs", 3, "CC BY-SA 4.0"),
    SourceEntry("Arduino - Language Reference", "https://www.arduino.cc/reference/en/", "arduino_docs", 3, "CC BY-SA 4.0"),
    SourceEntry("Arduino - Tutorials", "https://docs.arduino.cc/tutorials/", "arduino_docs", 3, "CC BY-SA 4.0"),
    SourceEntry("Arduino - Pinout Diagrams", "https://docs.arduino.cc/hardware/", "arduino_docs", 3, "CC BY-SA 4.0"),

    # ═══ RASPBERRY PI DOCUMENTATION ═══ (priority 4)
    SourceEntry("Raspberry Pi - Documentation", "https://www.raspberrypi.com/documentation/", "raspberry_pi_docs", 4, "CC BY-SA 4.0"),
    SourceEntry("Raspberry Pi - GPIO Usage", "https://www.raspberrypi.com/documentation/computers/raspberry-pi.html", "raspberry_pi_docs", 4, "CC BY-SA 4.0"),
    SourceEntry("Raspberry Pi - HAT Specification", "https://github.com/raspberrypi/hats", "raspberry_pi_docs", 4, "BSD-3-Clause"),

    # ═══ SPARKFUN ═══ (priority 5)
    SourceEntry("SparkFun - Tutorials", "https://learn.sparkfun.com/tutorials", "sparkfun", 5, "CC BY-SA 4.0"),
    SourceEntry("SparkFun - What is a Circuit?", "https://learn.sparkfun.com/tutorials/what-is-a-circuit", "sparkfun", 5, "CC BY-SA 4.0"),
    SourceEntry("SparkFun - How to Read a Schematic", "https://learn.sparkfun.com/tutorials/how-to-read-a-schematic", "sparkfun", 5, "CC BY-SA 4.0"),
    SourceEntry("SparkFun - Resistor Guide", "https://learn.sparkfun.com/tutorials/resistors", "sparkfun", 5, "CC BY-SA 4.0"),
    SourceEntry("SparkFun - Breadboard Guide", "https://learn.sparkfun.com/tutorials/how-to-use-a-breadboard", "sparkfun", 5, "CC BY-SA 4.0"),

    # ═══ ADAFRUIT ═══ (priority 6)
    SourceEntry("Adafruit - Learning System", "https://learn.adafruit.com", "adafruit", 6, "CC BY-SA 4.0"),
    SourceEntry("Adafruit - Arduino Lessons", "https://learn.adafruit.com/ladyadas-learn-arduino", "adafruit", 6, "CC BY-SA 4.0"),
    SourceEntry("Adafruit - Circuit Playground", "https://learn.adafruit.com/series-circuit-playground", "adafruit", 6, "CC BY-SA 4.0"),
    SourceEntry("Adafruit - Sensor Guide", "https://learn.adafruit.com/category/sensors", "adafruit", 6, "CC BY-SA 4.0"),

    # ═══ OPEN SOURCE CIRCUIT REFERENCES ═══ (priority 7)
    SourceEntry("OpenCircuits", "https://opencircuits.io", "open_source_circuit", 7, ""),
    SourceEntry("EasyEDA - Open Source Hardware", "https://easyeda.com", "open_source_circuit", 7, ""),
    SourceEntry("CircuitLab", "https://www.circuitlab.com", "open_source_circuit", 7, ""),

    # ═══ WIKIMEDIA COMMONS (images) ═══ (priority 8)
    SourceEntry("Wikimedia Commons - Electronics", "https://commons.wikimedia.org/wiki/Category:Electronic_component", "wikimedia_commons", 8, "CC BY-SA 4.0"),
    SourceEntry("Wikimedia Commons - Circuit Diagrams", "https://commons.wikimedia.org/wiki/Category:Circuit_diagrams", "wikimedia_commons", 8, "CC BY-SA 4.0"),
]


class SourceResolver:
    """Resolves and validates sources for AI-generated content."""

    def __init__(self, cache_dir: str = ".source_cache"):
        self.cache_dir = cache_dir
        self._source_map: dict[str, SourceEntry] = {}
        self._client = httpx.Client(timeout=5.0)
        self._build_index()
        os.makedirs(cache_dir, exist_ok=True)

    def _build_index(self):
        for src in PRIORITY_SOURCES:
            self._source_map[src.url] = src

    def get_by_url(self, url: str) -> Optional[SourceEntry]:
        return self._source_map.get(url)

    def search(self, query: str, limit: int = 10) -> list[SourceEntry]:
        """Search sources by title keyword."""
        q = query.lower()
        results = [
            s for s in PRIORITY_SOURCES if q in s.title.lower()
        ]
        return results[:limit]

    def get_by_type(self, source_type: str) -> list[SourceEntry]:
        """Get all sources of a given type."""
        return [s for s in PRIORITY_SOURCES if s.source_type == source_type]

    def get_by_category(self, category: str) -> list[SourceEntry]:
        """Get sources in a category (component, theory, platform, image)."""
        return [s for s in PRIORITY_SOURCES if s.category == category]

    def get_top_priority(self, count: int = 5) -> list[SourceEntry]:
        """Get the highest-priority sources."""
        return sorted(PRIORITY_SOURCES, key=lambda s: s.priority)[:count]

    def validate_url(self, url: str) -> bool:
        """Quick HTTP HEAD check to verify a URL is reachable."""
        if url in self._source_map:
            return True  # Trust curated sources
        try:
            resp = self._client.head(url, follow_redirects=True)
            return resp.status_code < 500
        except Exception:
            return False

    def format_sources_block(self, sources: list[SourceEntry]) -> str:
        """Generate an attribution block for LLM output."""
        lines = ["\n---", "**Sources:**"]
        seen = set()
        for s in sources:
            if s.url not in seen:
                seen.add(s.url)
                lic = f" — {s.license}" if s.license else ""
                lines.append(f"- [{s.title}]({s.url}){lic}")
        return "\n".join(lines)

    def to_json(self, sources: list[SourceEntry]) -> str:
        return json.dumps([s.to_dict() for s in sources], indent=2)


# Singleton
resolver = SourceResolver()
