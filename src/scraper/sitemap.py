from xml.etree import ElementTree as ET

import httpx

NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

# Orden = prioridad (productos primero, luego blog y servicios)
INCLUDE = (
    "/personas/productos/",
    "/personas/servicios-digitales/",
    "/personas/informacion-practica/",
    "/personas/servicio-al-consumidor-financiero/",
    "/personas/blog/",
    "/empresas/productos/",
)
EXCLUDE = (
    "simulador", "/herramientas/", "formulario", "/landing/",
    "/tarjetas/beneficios/", "investor-relations", ".content.html",
)


def get_urls(sitemap_url: str, client: httpx.Client) -> list[str]:
    resp = client.get(sitemap_url)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    return [loc.text.strip() for loc in root.findall(".//sm:loc", NS) if loc.text]


def _priority(url: str) -> int:
    return next(i for i, p in enumerate(INCLUDE) if p in url)


def filter_urls(urls: list[str], max_pages: int) -> list[str]:
    selected = [
        u for u in urls
        if any(p in u for p in INCLUDE) and not any(p in u for p in EXCLUDE)
    ]
    selected.sort(key=_priority)  
    return selected[:max_pages]