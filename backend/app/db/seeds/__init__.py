"""Database seeds package."""

import asyncio
from .seed_sources import seed as seed_sources

__all__ = ["seed_sources"]

if __name__ == "__main__":
    asyncio.run(seed_sources())
