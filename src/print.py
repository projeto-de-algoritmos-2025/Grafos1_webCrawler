import json
from graphviz import Digraph, Graph

with open("result.json", "r") as f:
    site_map = json.load(f)

# Cria um grafo dirigido
dot = Graph(comment='Mapa do Site')

# Adiciona nós
for node in site_map:
    dot.node(node)

# Adiciona arestas
for node, children in site_map.items():
    for child in children:
        dot.edge(node, child)

# Salva e renderiza (gera PNG)
dot.render('site_map', format='png', view=True)

