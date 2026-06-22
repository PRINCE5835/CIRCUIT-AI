"""Wikipedia API service for component knowledge."""
import httpx
import logging
import re

logger = logging.getLogger(__name__)

WIKI_API = "https://en.wikipedia.org/w/api.php"
WIKI_REST = "https://en.wikipedia.org/api/rest_v1"
USER_AGENT = "BreadBoardAI/0.1.0"


class WikipediaService:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=15.0, headers={"User-Agent": USER_AGENT})

    async def search(self, query: str, limit: int = 10) -> list[dict]:
        try:
            resp = await self.client.get(WIKI_API, params={
                "action": "query", "list": "search", "srsearch": query,
                "srlimit": limit, "format": "json", "origin": "*",
            })
            resp.raise_for_status()
            return [{
                "pageid": item["pageid"],
                "title": item["title"],
                "snippet": re.sub(r"<[^>]+>", "", item.get("snippet", "")),
                "url": f"https://en.wikipedia.org/wiki/{item['title'].replace(' ', '_')}",
            } for item in resp.json().get("query", {}).get("search", [])]
        except Exception as e:
            logger.error("Wikipedia search error: %s", e)
            return []

    async def get_summary(self, title: str) -> dict | None:
        try:
            resp = await self.client.get(f"{WIKI_REST}/page/summary/{title.replace(' ', '_')}")
            resp.raise_for_status()
            d = resp.json()
            return {
                "title": d.get("title", title), "extract": d.get("extract", ""),
                "url": f"https://en.wikipedia.org/wiki/{d.get('title', title).replace(' ', '_')}",
                "thumbnail": d.get("thumbnail", {}).get("source") if d.get("thumbnail") else None,
                "pageid": d.get("pageid"),
            }
        except Exception as e:
            logger.error("Wikipedia summary error: %s", e)
            return None

    async def get_component_info(self, name: str) -> dict | None:
        results = await self.search(f"{name} electronic component")
        if not results:
            results = await self.search(name)
        if not results:
            return None
        summary = await self.get_summary(results[0]["title"])
        if not summary:
            return None

        related = await self.search(f"{name} electronics", limit=5)
        return {
            "name": name,
            "wikipedia_title": summary["title"],
            "summary": summary["extract"][:2000],
            "url": summary["url"],
            "thumbnail": summary.get("thumbnail"),
            "pageid": summary["pageid"],
            "related": [{"title": r["title"], "url": r["url"]}
                        for r in related[1:6]
                        if r["title"].lower() != name.lower()],
        }

    async def get_details(self, name: str) -> dict | None:
        """Rich component info with specs, pinouts, applications."""
        summary = await self.get_component_info(name)
        if not summary:
            return None

        specs = await self.search(f"{name} specifications datasheet", limit=3)
        applications = await self.search(f"{name} application circuit uses", limit=3)
        alternatives = await self.search(f"{name} equivalent alternative", limit=3)

        return {
            **summary,
            "datasheets": [{"title": s["title"], "url": s["url"]} for s in specs],
            "applications": [{"title": a["title"], "url": a["url"]} for a in applications],
            "alternatives": [{"title": a["title"], "url": a["url"]} for a in alternatives
                             if a["title"].lower() != name.lower()],
        }

    async def close(self):
        await self.client.aclose()


wikipedia_service = WikipediaService()
