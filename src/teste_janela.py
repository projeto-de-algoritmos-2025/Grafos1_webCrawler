import tkinter as tk
from tkinter import ttk
import json
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import subprocess
import util
from urllib.parse import urlparse
import re
from collections import deque
import math

def rodar_aranha():
    spider = "paginas"
    project_dir = "/home/maubas/Documents/pa/Grafos1_webCrawler/scrapy/pages/"
    start_url = entrada.get()
    cmd = ["scrapy", "crawl", spider, "-a", f"start_url={start_url}", "-a","max_depth=2","-a","max_pages_per_layer=10"]
    subprocess.run(cmd, cwd=project_dir)


canvas = None  # variável global para o canvas

import json
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from urllib.parse import urlparse
import numpy as np

def mostrar_grafo_original_bonito():
    """Mostra o grafo original (spider.json) de forma bonita"""
    global canvas
    rodar_aranha()
    arquivo_spider = "./spider.json"  # Arquivo da spider original
    
    try:
        with open(arquivo_spider, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Arquivo '{arquivo_spider}' não encontrado! Execute a spider primeiro.")
        return
    
    G = nx.DiGraph()
    
    # Criar labels curtos e bonitos
    def criar_label_bonito(url):
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        
        if not path or path == "":
            return "🏠 HOME"
        
        # Pega a última parte da URL
        partes = path.split('/')
        nome = partes[-1] if partes else "página"
        
        # Remove extensões
        nome = nome.replace('.html', '').replace('.php', '').replace('.aspx', '')
        
        # Torna mais legível
        nome = nome.replace('-', ' ').replace('_', ' ').title()
        
        # Limita tamanho
        if len(nome) > 12:
            nome = nome[:12] + "..."
            
        return nome
    
    # Mapear URLs para labels
    url_para_label = {}
    for origem, destinos in data.items():
        if origem not in url_para_label:
            url_para_label[origem] = criar_label_bonito(origem)
        
        for destino in destinos:
            if destino not in url_para_label:
                url_para_label[destino] = criar_label_bonito(destino)
            
            G.add_edge(url_para_label[origem], url_para_label[destino])
    
    # Configurar figura
    fig, ax = plt.subplots(figsize=(16, 12))
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#ffffff')
    
    # Escolher layout baseado no tamanho
    num_nodes = len(G.nodes())
    
    if num_nodes <= 10:
        pos = nx.spring_layout(G, k=3, iterations=100, seed=42)
    elif num_nodes <= 25:
        pos = nx.kamada_kawai_layout(G)
    else:
        pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)
    
    # Calcular graus para tamanhos dos nós
    in_degrees = dict(G.in_degree())
    out_degrees = dict(G.out_degree())
    
    # Tamanhos dos nós baseados na importância
    node_sizes = []
    for node in G.nodes():
        importance = in_degrees[node] + out_degrees[node] + 1
        size = min(3000, max(1500, importance * 400))
        node_sizes.append(size)
    
    # Cores dos nós baseadas no tipo
    node_colors = []
    for node in G.nodes():
        if "🏠" in node:  # Home page
            node_colors.append('#ff6b6b')  # Vermelho para home
        elif out_degrees[node] > in_degrees[node]:  # Mais links saindo
            node_colors.append('#4ecdc4')  # Azul-verde para hubs
        elif in_degrees[node] > out_degrees[node]:  # Mais links chegando
            node_colors.append('#45b7d1')  # Azul para populares
        else:
            node_colors.append('#96ceb4')  # Verde claro para outros
    
    # Desenhar nós com borda
    nx.draw_networkx_nodes(
        G, pos,
        node_size=node_sizes,
        node_color=node_colors,
        alpha=0.9,
        edgecolors='#2c3e50',  # Borda escura
        linewidths=2,
        ax=ax
    )
    
    # Desenhar arestas com transparência
    nx.draw_networkx_edges(
        G, pos,
        edge_color='#7f8c8d',
        arrows=True,
        arrowsize=25,
        arrowstyle='-|>',
        alpha=0.6,
        width=2,
        connectionstyle="arc3,rad=0.1",  # Curva suave
        ax=ax
    )
    
    # Labels com fundo
    for node, (x, y) in pos.items():
        ax.text(x, y, node, 
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=9,
                fontweight='bold',
                color='white',
                bbox=dict(boxstyle="round,pad=0.3", 
                         facecolor='#2c3e50', 
                         alpha=0.8,
                         edgecolor='none'))
    
    # Título estilizado
    ax.set_title('🕸️ Grafo de Navegação do Site', 
                fontsize=20, 
                fontweight='bold', 
                color='#2c3e50',
                pad=20)
    
    ax.axis('off')
    
    # Legenda bonita
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#ff6b6b', 
                  markersize=15, label='🏠 Página Inicial'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#4ecdc4', 
                  markersize=15, label='🔗 Hub (muitos links)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#45b7d1', 
                  markersize=15, label='⭐ Popular (muito linkada)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#96ceb4', 
                  markersize=15, label='📄 Página comum')
    ]
    
    ax.legend(handles=legend_elements, 
             loc='upper left', 
             bbox_to_anchor=(0.02, 0.98),
             fontsize=12,
             frameon=True,
             facecolor='white',
             edgecolor='#2c3e50',
             framealpha=0.9)
    
    # Info box
    info_text = f"📊 Estatísticas:\n"
    info_text += f"• {len(G.nodes())} páginas\n"
    info_text += f"• {len(G.edges())} links\n"
    info_text += f"• Densidade: {nx.density(G):.2f}"
    
    ax.text(0.98, 0.02, info_text, 
           transform=ax.transAxes,
           verticalalignment='bottom',
           horizontalalignment='right',
           fontsize=11,
           bbox=dict(boxstyle="round,pad=0.5", 
                    facecolor='#ecf0f1', 
                    edgecolor='#2c3e50',
                    alpha=0.9))
    
    plt.tight_layout()
    
    if canvas:
        canvas.get_tk_widget().destroy()
    
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def mostrar_grafo_minimalista():
    """Versão super limpa e minimalista"""
    global canvas
    arquivo_spider = "../../src/spider.json"
    
    try:
        with open(arquivo_spider, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Arquivo '{arquivo_spider}' não encontrado!")
        return
    
    G = nx.DiGraph()
    
    # Labels numéricos simples
    urls = list(set(list(data.keys()) + [url for urls in data.values() for url in urls]))
    url_para_num = {url: f"{i+1}" for i, url in enumerate(urls)}
    
    for origem, destinos in data.items():
        for destino in destinos:
            G.add_edge(url_para_num[origem], url_para_num[destino])
    
    # Figura clean
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor('white')
    
    # Layout otimizado
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Desenho minimalista
    nx.draw(G, pos,
           with_labels=True,
           node_size=2000,
           node_color='#3498db',
           font_size=14,
           font_weight='bold',
           font_color='white',
           arrows=True,
           arrowsize=20,
           edge_color='#95a5a6',
           width=2,
           alpha=0.8,
           ax=ax)
    
    ax.set_title('Grafo do Site', fontsize=18, fontweight='bold', pad=20)
    ax.axis('off')
    
    # Lista de URLs na lateral
    url_list = "\n".join([f"{num}: {url.split('/')[-1]}" for url, num in list(url_para_num.items())[:15]])
    if len(url_para_num) > 15:
        url_list += f"\n... e mais {len(url_para_num) - 15}"
    
    ax.text(1.02, 1, url_list, transform=ax.transAxes,
           verticalalignment='top', fontsize=10,
           bbox=dict(boxstyle="round", facecolor='#ecf0f1', alpha=0.8))
    
    plt.tight_layout()
    
    if canvas:
        canvas.get_tk_widget().destroy()
    
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def mostrar_grafo_circular():
    """Layout circular elegante"""
    global canvas
    arquivo_spider = "../../src/spider.json"
    
    try:
        with open(arquivo_spider, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Arquivo '{arquivo_spider}' não encontrado!")
        return
    
    G = nx.DiGraph()
    
    # Criar grafo
    urls = list(set(list(data.keys()) + [url for urls in data.values() for url in urls]))
    url_para_num = {url: f"P{i+1}" for i, url in enumerate(urls)}
    
    for origem, destinos in data.items():
        for destino in destinos:
            G.add_edge(url_para_num[origem], url_para_num[destino])
    
    # Layout circular
    fig, ax = plt.subplots(figsize=(12, 12))
    pos = nx.circular_layout(G)
    
    # Gradiente de cores
    node_colors = plt.cm.Set3(np.linspace(0, 1, len(G.nodes())))
    
    nx.draw(G, pos,
           with_labels=True,
           node_size=2500,
           node_color=node_colors,
           font_size=12,
           font_weight='bold',
           arrows=True,
           arrowsize=25,
           edge_color='gray',
           width=1.5,
           alpha=0.9,
           ax=ax)
    
    ax.set_title('Grafo Circular', fontsize=18, fontweight='bold')
    ax.axis('off')
    
    plt.tight_layout()
    
    if canvas:
        canvas.get_tk_widget().destroy()
    
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def mostrar_grafo_arvore_bfs():
    rodar_aranha()
    grafo = util.abrir()
    ret = util.BFS(grafo, next(iter(grafo)))
    util.escreve(ret)
    
    global canvas
    arquivo = "result.json"
    
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Arquivo '{arquivo}' não encontrado!")
        return
    
    # Criar mapeamento URL -> Label
    url_para_num = {}
    num_para_url = {}
    contador = 0
    
    for origem, destinos in data.items():
        if origem not in url_para_num:
            url_para_num[origem] = f"P{contador}"
            num_para_url[f"P{contador}"] = origem
            contador += 1
        
        for destino in destinos:
            if destino not in url_para_num:
                url_para_num[destino] = f"P{contador}"
                num_para_url[f"P{contador}"] = destino
                contador += 1
    
    # Construir árvore BFS manualmente
    root_url = next(iter(data.keys()))
    root_node = url_para_num[root_url]
    
    # BFS para criar árvore (sem ciclos)
    visited = set()
    tree_edges = []
    queue = deque([root_url])
    visited.add(root_url)
    levels = {root_url: 0}
    
    while queue:
        current_url = queue.popleft()
        current_level = levels[current_url]
        
        if current_url in data:
            for neighbor_url in data[current_url]:
                if neighbor_url not in visited:
                    visited.add(neighbor_url)
                    levels[neighbor_url] = current_level + 1
                    queue.append(neighbor_url)
                    tree_edges.append((url_para_num[current_url], url_para_num[neighbor_url]))
    
    # Criar grafo da árvore
    G = nx.DiGraph()
    G.add_edges_from(tree_edges)
    
    # Layout manual em árvore
    pos = {}
    level_nodes = {}
    
    # Agrupar nós por nível
    for url, level in levels.items():
        node = url_para_num[url]
        if level not in level_nodes:
            level_nodes[level] = []
        level_nodes[level].append(node)
    
    max_level = max(level_nodes.keys()) if level_nodes else 0
    
    # Posicionar nós
    for level, nodes in level_nodes.items():
        y = max_level - level  # Níveis superiores ficam mais em cima
        num_nodes = len(nodes)
        
        if num_nodes == 1:
            pos[nodes[0]] = (0, y)
        else:
            # Distribuir horizontalmente
            width = max(4, num_nodes * 1.5)
            for i, node in enumerate(nodes):
                x = (i - (num_nodes - 1) / 2) * (width / num_nodes)
                pos[node] = (x, y)
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Cores por nível
    node_colors = []
    for node in G.nodes():
        url = num_para_url[node]
        level = levels[url]
        # Usar colormap baseado no nível
        color = plt.cm.RdYlBu(level / max_level if max_level > 0 else 0)
        node_colors.append(color)
    
    # Desenhar árvore
    nx.draw_networkx_nodes(
        G, pos,
        node_size=2500,
        node_color=node_colors,
        alpha=0.9,
        ax=ax
    )
    
    nx.draw_networkx_edges(
        G, pos,
        edge_color="gray",
        arrows=True,
        arrowsize=25,
        arrowstyle="->",
        alpha=0.7,
        width=2,
        ax=ax
    )
    
    nx.draw_networkx_labels(
        G, pos,
        font_size=12,
        font_weight="bold",
        font_color="black",
        ax=ax
    )
    
    ax.set_title("Árvore BFS - Layout Hierárquico Real", fontsize=16, fontweight="bold")
    ax.axis('off')
    
    # Legenda com níveis
    legend_text = "NÍVEIS BFS:\n"
    for level in sorted(level_nodes.keys()):
        nodes_in_level = [num_para_url[node] for node in level_nodes[level]]
        legend_text += f"Nível {level}: {len(nodes_in_level)} páginas\n"
    
    # Adicionar URLs na legenda
    legend_text += "\nMAPEAMENTO:\n"
    for node, url in list(num_para_url.items())[:10]:
        legend_text += f"{node}: {url.split('/')[-1]}\n"
    
    if len(num_para_url) > 10:
        legend_text += f"... e mais {len(num_para_url) - 10} páginas"
    
    ax.text(1.02, 1, legend_text, transform=ax.transAxes, 
            verticalalignment='top', fontsize=9,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
    
    plt.tight_layout()
    
    if canvas:
        canvas.get_tk_widget().destroy()
    
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def botao_extra1():
    print("Botão Extra 1 clicado!")

def botao_extra2():
    rodar_aranha()
    grafo = util.abrir()
    ret = util.DFS(grafo, next(iter(grafo)))
    util.escreve(ret)
    
    global canvas
    arquivo = "result.json"
    
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Arquivo '{arquivo}' não encontrado!")
        return
    
    # Criar mapeamento URL -> Label
    url_para_num = {}
    num_para_url = {}
    contador = 0
    
    for origem, destinos in data.items():
        if origem not in url_para_num:
            url_para_num[origem] = f"P{contador}"
            num_para_url[f"P{contador}"] = origem
            contador += 1
        
        for destino in destinos:
            if destino not in url_para_num:
                url_para_num[destino] = f"P{contador}"
                num_para_url[f"P{contador}"] = destino
                contador += 1
    
    # Construir árvore BFS manualmente
    root_url = next(iter(data.keys()))
    root_node = url_para_num[root_url]
    
    # BFS para criar árvore (sem ciclos)
    visited = set()
    tree_edges = []
    queue = deque([root_url])
    visited.add(root_url)
    levels = {root_url: 0}
    
    while queue:
        current_url = queue.popleft()
        current_level = levels[current_url]
        
        if current_url in data:
            for neighbor_url in data[current_url]:
                if neighbor_url not in visited:
                    visited.add(neighbor_url)
                    levels[neighbor_url] = current_level + 1
                    queue.append(neighbor_url)
                    tree_edges.append((url_para_num[current_url], url_para_num[neighbor_url]))
    
    # Criar grafo da árvore
    G = nx.DiGraph()
    G.add_edges_from(tree_edges)
    
    # Layout manual em árvore
    pos = {}
    level_nodes = {}
    
    # Agrupar nós por nível
    for url, level in levels.items():
        node = url_para_num[url]
        if level not in level_nodes:
            level_nodes[level] = []
        level_nodes[level].append(node)
    
    max_level = max(level_nodes.keys()) if level_nodes else 0
    
    # Posicionar nós
    for level, nodes in level_nodes.items():
        y = max_level - level  # Níveis superiores ficam mais em cima
        num_nodes = len(nodes)
        
        if num_nodes == 1:
            pos[nodes[0]] = (0, y)
        else:
            # Distribuir horizontalmente
            width = max(4, num_nodes * 1.5)
            for i, node in enumerate(nodes):
                x = (i - (num_nodes - 1) / 2) * (width / num_nodes)
                pos[node] = (x, y)
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Cores por nível
    node_colors = []
    for node in G.nodes():
        url = num_para_url[node]
        level = levels[url]
        # Usar colormap baseado no nível
        color = plt.cm.RdYlBu(level / max_level if max_level > 0 else 0)
        node_colors.append(color)
    
    # Desenhar árvore
    nx.draw_networkx_nodes(
        G, pos,
        node_size=2500,
        node_color=node_colors,
        alpha=0.9,
        ax=ax
    )
    
    nx.draw_networkx_edges(
        G, pos,
        edge_color="gray",
        arrows=True,
        arrowsize=25,
        arrowstyle="->",
        alpha=0.7,
        width=2,
        ax=ax
    )
    
    nx.draw_networkx_labels(
        G, pos,
        font_size=12,
        font_weight="bold",
        font_color="black",
        ax=ax
    )
    
    ax.set_title("Árvore DFS", fontsize=16, fontweight="bold")
    ax.axis('off')
    
    # Legenda com níveis
    legend_text = "NÍVEIS DFS:\n"
    for level in sorted(level_nodes.keys()):
        nodes_in_level = [num_para_url[node] for node in level_nodes[level]]
        legend_text += f"Nível {level}: {len(nodes_in_level)} páginas\n"
    
    # Adicionar URLs na legenda
    legend_text += "\nMAPEAMENTO:\n"
    for node, url in list(num_para_url.items())[:10]:
        legend_text += f"{node}: {url.split('/')[-1]}\n"
    
    if len(num_para_url) > 10:
        legend_text += f"... e mais {len(num_para_url) - 10} páginas"
    
    ax.text(1.02, 1, legend_text, transform=ax.transAxes, 
            verticalalignment='top', fontsize=9,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
    
    plt.tight_layout()
    
    if canvas:
        canvas.get_tk_widget().destroy()
    
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Criar janela
janela = tk.Tk()
janela.title("Visualização do Grafo")
janela.geometry("900x600")

# Campo de input
label = ttk.Label(janela, text="Nome do arquivo JSON:")
label.pack(pady=5)

entrada = ttk.Entry(janela, width=40)
entrada.insert(0, "https://quotes.toscrape.com/")
entrada.pack(pady=5)

# Frame para os botões
frame_botoes = ttk.Frame(janela)
frame_botoes.pack(pady=10)

# Botões lado a lado
botao_mostrar = ttk.Button(frame_botoes, text="Mostrar BFS", command=mostrar_grafo_arvore_bfs)
botao_mostrar.pack(side=tk.LEFT, padx=5)

botao1 = ttk.Button(frame_botoes, text="Mostrar DFS", command=botao_extra2)
botao1.pack(side=tk.LEFT, padx=5)

botao2 = ttk.Button(frame_botoes, text="Mostrar Grafo original", command=mostrar_grafo_original_bonito)
botao2.pack(side=tk.LEFT, padx=5)

janela.mainloop()

