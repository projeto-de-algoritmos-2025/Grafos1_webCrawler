# Grafos 1 - Web Crawler

Este projeto implementa um **Web Crawler** em Python, com o objetivo de construir um **grafo de páginas acessíveis a partir de uma URL inicial**.  
A partir do grafo gerado, aplicamos algoritmos clássicos de **busca em largura (BFS)** e **busca em profundidade (DFS)**, permitindo visualizar e analisar a estrutura de links de um site.

---

## Tecnologias Utilizadas
- [Python 3.10+](https://www.python.org/)
- [Scrapy](https://scrapy.org/) (coleta de páginas e links)
- [Graphviz](https://graphviz.org/) (visualização do grafo)
- Algoritmos de **BFS**, **DFS** e busca de caminho


##  Como Executar

### 1. Instalar dependências
Recomendado criar um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate
pip install scrapy graphviz
```

> É necessário ter o **Graphviz** instalado no sistema:
- Linux (Debian/Ubuntu): `sudo apt install graphviz`
- Fedora: `sudo dnf install graphviz`
- MacOS: `brew install graphviz`
- Windows: [Download aqui](https://graphviz.gitlab.io/download/)


### 2. Rodar o Web Crawler
Exemplo com o site de testes:
```bash
scrapy crawl paginas -a start_url="https://quotes.toscrape.com/page/1/"
```
Isso gera o arquivo `grafo.json` com o mapeamento de links.

## Autores

Projeto desenvolvido como trabalho da disciplina de **Projeto de Algoritmos**.

Dupla responsável: 

- [Júlia Fortunato](https://github.com/julia-fortunato)  
- [Maurício Ferreira](https://github.com/mauricio_araujoo)  

## Vídeo de apresentação
