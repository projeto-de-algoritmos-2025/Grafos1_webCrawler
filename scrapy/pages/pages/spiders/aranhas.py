from urllib.parse import urlparse, urljoin
from pathlib import Path
import scrapy
import json


class Aranhas(scrapy.Spider):
    name = "paginas"

    def __init__(self, start_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [start_url] if start_url else []
        self.visited = set()
        self.grafo = {}

    def parse(self, response):
        page = response.url
        self.visited.add(page)
        links = set()

        base_url = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(response.url))

        for href in response.css('a::attr(href)').getall():
            full_url = urljoin(base_url, href).split("#")[0]  # remove anchors
            if full_url.startswith(base_url) and full_url not in self.visited:
                links.add(full_url)
                yield scrapy.Request(full_url, callback=self.parse)

        self.grafo[page] = list(links)
        self.log(f"Página: {page} -> Links: {links}")

    def closed(self, reason):
        Path("./grafo.json").write_text(json.dumps(self.grafo, indent=2))
