"""Seed script to populate priority sources into the database."""

import asyncio
from app.db.base import async_session_factory
from app.models.source import SourceType
from app.services.source_service import SourceService

SEED_SOURCES = [
    # Wikipedia
    {
        "title": "Wikipedia - Ohm's Law",
        "url": "https://en.wikipedia.org/wiki/Ohm%27s_law",
        "source_type": SourceType.WIKIPEDIA,
        "priority": 1,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "Wikipedia - Kirchhoff's Circuit Laws",
        "url": "https://en.wikipedia.org/wiki/Kirchhoff%27s_circuit_laws",
        "source_type": SourceType.WIKIPEDIA,
        "priority": 1,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "Wikipedia - Resistor",
        "url": "https://en.wikipedia.org/wiki/Resistor",
        "source_type": SourceType.WIKIPEDIA,
        "priority": 1,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "Wikipedia - Capacitor",
        "url": "https://en.wikipedia.org/wiki/Capacitor",
        "source_type": SourceType.WIKIPEDIA,
        "priority": 1,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "Wikipedia - Inductor",
        "url": "https://en.wikipedia.org/wiki/Inductor",
        "source_type": SourceType.WIKIPEDIA,
        "priority": 1,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "Wikipedia - Diode",
        "url": "https://en.wikipedia.org/wiki/Diode",
        "source_type": SourceType.WIKIPEDIA,
        "priority": 1,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "Wikipedia - Transistor",
        "url": "https://en.wikipedia.org/wiki/Transistor",
        "source_type": SourceType.WIKIPEDIA,
        "priority": 1,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "Wikipedia - Operational Amplifier",
        "url": "https://en.wikipedia.org/wiki/Operational_amplifier",
        "source_type": SourceType.WIKIPEDIA,
        "priority": 1,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "Wikipedia - 555 Timer IC",
        "url": "https://en.wikipedia.org/wiki/555_timer_IC",
        "source_type": SourceType.WIKIPEDIA,
        "priority": 1,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "Wikipedia - Arduino",
        "url": "https://en.wikipedia.org/wiki/Arduino",
        "source_type": SourceType.WIKIPEDIA,
        "priority": 1,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "Wikipedia - Raspberry Pi",
        "url": "https://en.wikipedia.org/wiki/Raspberry_Pi",
        "source_type": SourceType.WIKIPEDIA,
        "priority": 1,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "Wikipedia - Breadboard",
        "url": "https://en.wikipedia.org/wiki/Breadboard",
        "source_type": SourceType.WIKIPEDIA,
        "priority": 1,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "Wikipedia - Series and Parallel Circuits",
        "url": "https://en.wikipedia.org/wiki/Series_and_parallel_circuits",
        "source_type": SourceType.WIKIPEDIA,
        "priority": 1,
        "license": "CC BY-SA 4.0",
    },
    # Electronics Tutorials
    {
        "title": "Electronics Tutorials",
        "url": "https://www.electronics-tutorials.ws",
        "source_type": SourceType.ELECTRONICS_TUTORIALS,
        "priority": 2,
        "license": "",
    },
    {
        "title": "Electronics Tutorials - RC Networks",
        "url": "https://www.electronics-tutorials.ws/rc/rc_1.html",
        "source_type": SourceType.ELECTRONICS_TUTORIALS,
        "priority": 2,
        "license": "",
    },
    {
        "title": "Electronics Tutorials - Op-amp Basics",
        "url": "https://www.electronics-tutorials.ws/opamp/opamp_1.html",
        "source_type": SourceType.ELECTRONICS_TUTORIALS,
        "priority": 2,
        "license": "",
    },
    # Arduino
    {
        "title": "Arduino Documentation",
        "url": "https://docs.arduino.cc/",
        "source_type": SourceType.ARDUINO_DOCS,
        "priority": 3,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "Arduino Language Reference",
        "url": "https://www.arduino.cc/reference/en/",
        "source_type": SourceType.ARDUINO_DOCS,
        "priority": 3,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "Arduino Tutorials",
        "url": "https://docs.arduino.cc/tutorials/",
        "source_type": SourceType.ARDUINO_DOCS,
        "priority": 3,
        "license": "CC BY-SA 4.0",
    },
    # Raspberry Pi
    {
        "title": "Raspberry Pi Documentation",
        "url": "https://www.raspberrypi.com/documentation/",
        "source_type": SourceType.RASPBERRY_PI_DOCS,
        "priority": 4,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "Raspberry Pi GPIO",
        "url": "https://www.raspberrypi.com/documentation/computers/raspberry-pi.html",
        "source_type": SourceType.RASPBERRY_PI_DOCS,
        "priority": 4,
        "license": "CC BY-SA 4.0",
    },
    # SparkFun
    {
        "title": "SparkFun Tutorials",
        "url": "https://learn.sparkfun.com/tutorials",
        "source_type": SourceType.SPARKFUN,
        "priority": 5,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "SparkFun - How to Read a Schematic",
        "url": "https://learn.sparkfun.com/tutorials/how-to-read-a-schematic",
        "source_type": SourceType.SPARKFUN,
        "priority": 5,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "SparkFun - Resistors",
        "url": "https://learn.sparkfun.com/tutorials/resistors",
        "source_type": SourceType.SPARKFUN,
        "priority": 5,
        "license": "CC BY-SA 4.0",
    },
    # Adafruit
    {
        "title": "Adafruit Learning System",
        "url": "https://learn.adafruit.com",
        "source_type": SourceType.ADAFRUIT,
        "priority": 6,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "Adafruit - Arduino Lessons",
        "url": "https://learn.adafruit.com/ladyadas-learn-arduino",
        "source_type": SourceType.ADAFRUIT,
        "priority": 6,
        "license": "CC BY-SA 4.0",
    },
    # Open Source Circuits
    {
        "title": "EasyEDA",
        "url": "https://easyeda.com",
        "source_type": SourceType.OPEN_SOURCE_CIRCUIT,
        "priority": 7,
        "license": "",
    },
    {
        "title": "CircuitLab",
        "url": "https://www.circuitlab.com",
        "source_type": SourceType.OPEN_SOURCE_CIRCUIT,
        "priority": 7,
        "license": "",
    },
    # Wikimedia Commons (images)
    {
        "title": "Wikimedia Commons - Electronics",
        "url": "https://commons.wikimedia.org/wiki/Category:Electronic_components",
        "source_type": SourceType.WIKIMEDIA_COMMONS,
        "priority": 8,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "Wikimedia Commons - Circuit Diagrams",
        "url": "https://commons.wikimedia.org/wiki/Category:Circuit_diagrams",
        "source_type": SourceType.WIKIMEDIA_COMMONS,
        "priority": 8,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "Wikipedia Commons - Arduino",
        "url": "https://commons.wikimedia.org/wiki/Category:Arduino",
        "source_type": SourceType.WIKIPEDIA_COMMONS,
        "priority": 8,
        "license": "CC BY-SA 4.0",
    },
    {
        "title": "Wikipedia Commons - Raspberry Pi",
        "url": "https://commons.wikimedia.org/wiki/Category:Raspberry_Pi",
        "source_type": SourceType.WIKIPEDIA_COMMONS,
        "priority": 8,
        "license": "CC BY-SA 4.0",
    },
]


async def seed():
    async with async_session_factory() as session:
        service = SourceService(session)
        for data in SEED_SOURCES:
            exists = await service.source_repo.exists(url=data["url"])
            if not exists:
                await service.source_repo.create(**data)
                print(f"  + {data['title']}")
            else:
                print(f"  ~ {data['title']} (exists)")
        await session.commit()
    print(f"\nSeeded {len(SEED_SOURCES)} sources.")


if __name__ == "__main__":
    asyncio.run(seed())
