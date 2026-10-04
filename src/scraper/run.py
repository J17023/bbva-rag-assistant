import logging
import time
from pathlib import Path

import httpx

from src.config import settings
from src.scraper.fetcher import HEADERS, fetch_page, save_raw, url_to_slug
from src.scraper.sitemap import filter_urls, get_urls

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("scraper")


def main() -> None:
    with httpx.Client(headers=HEADERS, timeout=settings.request_timeout, follow_redirects=True) as client:
        urls = filter_urls(get_urls(f"{settings.base_url}/sitemap.xml", client), settings.max_pages)
        logger.info("URLs seleccionadas: %d", len(urls))

        ok = failed = skipped = 0
        for i, url in enumerate(urls, 1):
            if (Path(settings.raw_dir) / f"{url_to_slug(url)}.html").exists():
                skipped += 1
                continue
            html = fetch_page(client, url)
            if html:
                save_raw(url, html, settings.raw_dir)
                ok += 1
            else:
                failed += 1
            logger.info("[%d/%d] %s", i, len(urls), url)
            time.sleep(settings.request_delay)

    logger.info("Terminado: %d descargadas, %d fallidas, %d ya existían", ok, failed, skipped)


if __name__ == "__main__":
    main()