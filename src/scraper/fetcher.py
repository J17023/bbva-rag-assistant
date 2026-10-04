import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; bbva-rag-assistant/0.1)"}


def url_to_slug(url: str) -> str:
    path = url.split("bbva.com.co")[-1].strip("/").removesuffix(".html")
    return path.replace("/", "__") or "home"


def fetch_page(client: httpx.Client, url: str, retries: int = 3) -> str | None:
    for attempt in range(1, retries + 1):
        try:
            resp = client.get(url)
            resp.raise_for_status()
            return resp.text
        except httpx.HTTPError as e:
            logger.warning("Intento %d/%d falló para %s: %s", attempt, retries, url, e)
            time.sleep(2 * attempt)
    logger.error("No se pudo descargar %s", url)
    return None


def save_raw(url: str, html: str, raw_dir: str) -> None:
    out = Path(raw_dir)
    out.mkdir(parents=True, exist_ok=True)
    slug = url_to_slug(url)
    (out / f"{slug}.html").write_text(html, encoding="utf-8")
    meta = {
        "url": url,
        "slug": slug,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "size_bytes": len(html.encode("utf-8")),
    }
    (out / f"{slug}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")