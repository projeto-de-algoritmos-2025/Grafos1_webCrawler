import tkinter as tk
from tkinter import ttk
import json
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import subprocess
from urllib.parse import urlparse
import re
from collections import deque
import numpy as np
from collections import deque

canvas = None  # variável global para o canvas

def rodar_aranha():
    spider = "paginas_controlada"
    project_dir = "/home/julia/Documentos/PA/Grafos1_webCrawler/scrapy/pages"
    start_url = entrada.get()
    cmd = ["scrapy", "crawl", spider, "-a", f"start_url={start_url}", "-a","max_depth=2","-a","max_pages_per_layer=10"]
    subprocess.run(cmd, cwd=project_dir)
    mostrar_grafo_circular()

def mostrar_grafo_circular():
    """Layout circular elegante"""
    global canvas

    data = limpar_e_carregar_json("./spider.json")

    
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

def limpar_e_carregar_json(caminho_arquivo):
    """
    Carrega e limpa arquivo JSON que pode ter dados extras ou malformações
    """
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
        
        # Tenta carregar normalmente primeiro
        try:
            return json.loads(conteudo)
        except json.JSONDecodeError as e:
            
            # Tenta encontrar o primeiro objeto JSON válido
            stack = []
            start_idx = -1
            end_idx = -1
            
            for i, char in enumerate(conteudo):
                if char == '{':
                    if start_idx == -1:
                        start_idx = i
                    stack.append(char)
                elif char == '}':
                    if stack:
                        stack.pop()
                        if not stack and start_idx != -1:
                            end_idx = i
                            break
            
            if start_idx != -1 and end_idx != -1:
                json_valido = conteudo[start_idx:end_idx + 1]
                print(f" Tentando extrair JSON válido (caracteres {start_idx} a {end_idx})")
                return json.loads(json_valido)
            
            
            # Procura padrões de início e fim de objeto JSON
            match = re.search(r'\{.*\}', conteudo, re.DOTALL)
            if match:
                return json.loads(match.group())
            
            raise Exception("Não foi possível extrair JSON válido do arquivo")
            
    except FileNotFoundError:
        print(f"Arquivo '{caminho_arquivo}' não encontrado!")
        return None
    except Exception as e:
        print(f" Erro ao processar JSON: {e}")
        return None


def BFS(grafo, inicio):
    
    if not grafo or inicio not in grafo:
        return {}
    
    pais = {inicio: None}
    fila = deque([inicio])
    
    while fila:
        atual = fila.popleft()
        
        for vizinho in grafo.get(atual, []):
            if vizinho not in pais:
                pais[vizinho] = atual
                fila.append(vizinho)
                
    # Converte a estrutura de 'filho: pai' para 'pai: [filhos]'
    arvore_bfs_visual = {}
    for no, pai in pais.items():
        if pai is not None:
            if pai not in arvore_bfs_visual:
                arvore_bfs_visual[pai] = []
            arvore_bfs_visual[pai].append(no)
            
    return arvore_bfs_visual

def mostrar_grafo_arvore_bfs():

    global canvas

    grafo = limpar_e_carregar_json("spider.json")
    
    if not grafo:
        return

    inicio = next(iter(grafo))
    arvore_bfs = BFS(grafo, inicio)
    
    if not arvore_bfs:
        return
    
    try:
        with open("result.json", "w", encoding="utf-8") as f:
            json.dump(arvore_bfs, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(e)
    
    data = arvore_bfs
    
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
    
    root_url = next(iter(data.keys()))
    root_node = url_para_num[root_url]
    
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
    
    G = nx.DiGraph()
    if tree_edges:
        G.add_edges_from(tree_edges)
    else:
        G.add_node(root_node)
    
    pos = {}
    level_nodes = {}
    
    for url, level in levels.items():
        node = url_para_num[url]
        if level not in level_nodes:
            level_nodes[level] = []
        level_nodes[level].append(node)
    
    max_level = max(level_nodes.keys()) if level_nodes else 0

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
    fig.patch.set_facecolor('white')
    
    if G.nodes():
        # Cores por nível
        node_colors = []
        for node in G.nodes():
            url = num_para_url[node]
            level = levels.get(url, 0)
            # Usar colormap baseado no nível
            color = plt.cm.RdYlBu(level / max_level if max_level > 0 else 0)
            node_colors.append(color)
        
        # Desenhar árvore
        nx.draw_networkx_nodes(
            G, pos,
            node_size=2500,
            node_color="black",
            alpha=0.9,
            edgecolors='black',
            linewidths=1,
            ax=ax
        )
        
        if G.edges():
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
            font_size=10,
            font_weight="bold",
            font_color="white",
            ax=ax
        )
    
    ax.set_title(" Árvore BFS - Layout Hierárquico", fontsize=16, fontweight="bold", pad=20)
    ax.axis('off')
    
    # Legenda com níveis
    legend_text = "NÍVEIS BFS:\n"
    for level in sorted(level_nodes.keys()):
        nodes_in_level = [num_para_url[node] for node in level_nodes[level]]
        legend_text += f"Nível {level}: {len(nodes_in_level)} páginas\n"
    
    # Adicionar URLs na legenda (limitado para não sobrecarregar)
    legend_text += "\nMAPEAMENTO (primeiros 8):\n"
    items_mostrados = list(num_para_url.items())[:8]
    for node, url in items_mostrados:
        # Pegar apenas a parte final da URL
        url_parts = url.split('/')
        url_short = url_parts[-1] if url_parts[-1] else url_parts[-2] if len(url_parts) > 1 else url
        legend_text += f"{node}: {url_short[:20]}...\n" if len(url_short) > 20 else f"{node}: {url_short}\n"
    
    if len(num_para_url) > 8:
        legend_text += f"... e mais {len(num_para_url) - 8} páginas"
    
    ax.text(1.02, 1, legend_text, transform=ax.transAxes, 
            verticalalignment='top', fontsize=9,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
    
    plt.tight_layout()
    
    # Atualizar canvas
    if 'canvas' in globals() and canvas:
        canvas.get_tk_widget().destroy()
    
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


janela = tk.Tk()
janela.title("Visualização do Grafo")
janela.geometry("900x600")

label = ttk.Label(janela, text="URL do site:")
label.pack(pady=5)

# Novo frame para agrupar o input e o botão "Gerar"
frame_input_botao = ttk.Frame(janela)
frame_input_botao.pack(pady=5)

entrada = ttk.Entry(frame_input_botao, width=40)
entrada.insert(0, "")
entrada.pack(side=tk.LEFT, padx=5)

botao_gerar = ttk.Button(frame_input_botao, text="Gerar", command=rodar_aranha)
botao_gerar.pack(side=tk.LEFT, padx=5)

frame_botoes = ttk.Frame(janela)
frame_botoes.pack(pady=10)

botao_mostrar = ttk.Button(frame_botoes, text="Mostrar BFS", command=mostrar_grafo_arvore_bfs)
botao_mostrar.pack(side=tk.LEFT, padx=5)

botao2 = ttk.Button(frame_botoes, text="Mostrar Grafo original", command=mostrar_grafo_circular)
botao2.pack(side=tk.LEFT, padx=5)

janela.mainloop()


