import json

with open("site_map.json", "r") as f:
    site_map = json.load(f)

def BFS(g, init):
    visit = set()
    ret = {}
    queue = []
    queue.append(init)
    visit.add(init)

    for node in g:
        ret[node] = []
    
    while queue:
        atual = queue.pop(0)
        for node in g[atual]:
            if node not in visit:
                visit.add(node)
                queue.append(node)
                ret[atual].append(node) 
    

    return ret


resultado = BFS(site_map, next(iter(site_map)))

with open("result.json", "w") as f:
    json.dump(resultado, f, indent=4)
