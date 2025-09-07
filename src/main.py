import json

with open("site_map.json", "r") as f:
    site_map = json.load(f)

def BFS(g, init):
    visit = set()
    ret = {}
    queue = [init]
    visit.add(init)

    for node in g:
        ret[node] = []

    while queue:
        atual = queue.pop(0)
        for node in g.get(atual, []):   # <--- evita KeyError
            if node not in visit:
                visit.add(node)
                queue.append(node)
                ret[atual].append(node)

    return ret

def DFS(g, init, visit=None, ret=None):
    if visit is None:
        visit = set()
    if ret is None:
        ret = {}
        for node in g:
            ret[node] = []

    visit.add(init)

    for node in g[init]:
        if node not in visit:
            ret[init].append(node)
            DFS(g, node, visit, ret)
    
    return ret

def reverse_graph(g):
    rev = {}
    for node in g:
        rev[node] = []
    
    for node in g:
        for neighbor in g[node]:
            rev[neighbor].append(node)
    
    return rev

def BFS_node_to_other(g, start, end):
    visit = set()
    queue = []
    queue.append((start, [start]))
    visit.add(start)

    while queue:
        atual, path = queue.pop(0)
        if atual == end:
            return path
        for node in g[atual]:
            if node not in visit:
                visit.add(node)
                queue.append((node, path + [node]))
    
    return None

resultado = BFS(site_map, "https://quotes.toscrape.com/page/1/")


with open("result.json", "w") as f:
    json.dump(resultado, f, indent=4)

