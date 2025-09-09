from urllib.parse import urlparse, urljoin
from pathlib import Path
import scrapy
import json
from collections import deque

class AranhasControlada(scrapy.Spider):
    name = "paginas_controlada"
    
    def __init__(self, start_url=None, max_depth=3, max_pages_per_layer=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [start_url] if start_url else []
        self.max_depth = int(max_depth)
        self.max_pages_per_layer = int(max_pages_per_layer)
        
        
        self.grafo = {}
        self.visited = set()
        self.nivel_atual = 0
        self.fila_por_nivel = {}  # {nivel: [urls]}
        
       
        for i in range(self.max_depth + 1):
            self.fila_por_nivel[i] = []
        
        if start_url:
            self.fila_por_nivel[0] = [start_url]
    
    def start_requests(self):
        
        if self.fila_por_nivel[0]:
            for url in self.fila_por_nivel[0]:
                yield scrapy.Request(url, callback=self.parse, meta={'depth': 0})
    
    def parse(self, response):
        depth = response.meta.get('depth', 0)
        url = response.url
        
        if depth > self.max_depth or url in self.visited:
            return
        
        self.visited.add(url)
        
        # Extrai links
        base_url = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(url))
        links = []
        
        for href in response.css('a::attr(href)').getall():
            full_url = urljoin(base_url, href).split('#')[0].rstrip('/')
            
            if (full_url.startswith(base_url) and 
                full_url != url and 
                full_url not in self.visited):
                links.append(full_url)
        
        # Remove duplicatas e limita
        links = list(dict.fromkeys(links))[:self.max_pages_per_layer]
        self.grafo[url] = links
        
        # Adiciona ao próximo nível
        next_depth = depth + 1
        if next_depth <= self.max_depth:
            for link in links:
                if link not in self.visited and link not in self.fila_por_nivel[next_depth]:
                    self.fila_por_nivel[next_depth].append(link)
            
            # Processa próximo nível
            for link in self.fila_por_nivel[next_depth]:
                if link not in self.visited:
                    yield scrapy.Request(link, callback=self.parse, meta={'depth': next_depth})
    
    def closed(self, reason):
        # Salva resultado
        with open("../../src/spider.json", 'w', encoding='utf-8') as f:
            json.dump(self.grafo, f, indent=2, ensure_ascii=False)
        