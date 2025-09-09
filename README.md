# Grafos 1 - Web Crawler

Este projeto implementa um **Web Crawler** em Python, com o objetivo de construir um **grafo de páginas acessíveis a partir de uma URL inicial**.  
A partir do grafo gerado, aplicamos algoritmos clássicos de **busca em largura (BFS)**, permitindo visualizar e analisar a estrutura de links de um site.

---

## Tecnologias Utilizadas
- [Python 3.10+](https://www.python.org/)
- [Scrapy](https://scrapy.org/) (coleta de páginas e links)
- [Graphviz](https://graphviz.org/) (visualização do grafo)
- Algoritmo de **BFS** e de visualização geral do grafo


##  Como Executar

### 1. Instalar dependências
Recomendado criar um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate
make install
```

> É necessário ter o **Graphviz e o TKinter** instalado no sistema:
- Linux (Debian/Ubuntu): `sudo apt install graphviz`
- Fedora: `sudo dnf install graphviz`
- MacOS: `brew install graphviz`
- Windows: [Download aqui](https://graphviz.gitlab.io/download/)
- TKinter: [Segue Documentação](https://tkdocs.com/tutorial/install.html)


### 2. Rodar o Web Crawler
Exemplo com o site escolhido:
```bash
make
```
Após isso, deve-se apenas inserir uma URL no input gerado na tela, clicar em 'Gerar', aguardar a finalização da execução do scrapy, e então escolher visualizar a BFS ou o grafo geral.

## Autores

Dupla responsável: 21

- [Júlia Fortunato](https://github.com/julia-fortunato)  
- [Maurício Ferreira](https://github.com/mauricio_araujoo)  

## Vídeo de apresentação

- [Video de apresentação](https://www.youtube.com/watch?v=F954oB1af_k)
