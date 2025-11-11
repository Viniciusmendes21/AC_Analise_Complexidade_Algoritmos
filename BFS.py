from collections import deque


def BFS(arestas, direcionado=False, inicio=None):
    g = {}
    if isinstance(arestas, dict):
        for k, vs in arestas.items():
            u = str(k).strip()
            if not u:
                continue
            for v in vs:
                if v is None:
                    continue
                nv = str(v).strip()
                if nv:
                    g.setdefault(u, []).append(nv)
        if not direcionado:
            for u, nbrs in list(g.items()):
                for v in nbrs:
                    if u not in g.setdefault(v, []):
                        g[v].append(u)
    else:
        tokens = arestas.split(',') if isinstance(arestas, str) else list(arestas)
        for tok in tokens:
            if tok is None:
                continue
            if isinstance(tok, (list, tuple)) and len(tok) >= 2:
                a, b = str(tok[0]).strip(), str(tok[1]).strip()
            else:
                s = str(tok).strip()
                if not s:
                    continue
                if '-' in s:
                    a, b = (p.strip() for p in s.split('-', 1))
                else:
                    g.setdefault(s, [])
                    continue
            if not a or not b:
                continue
            if a == b:
                g.setdefault(a, []).append(b)
            else:
                g.setdefault(a, []).append(b)
                if not direcionado:
                    g.setdefault(b, []).append(a)

    componentes = []
    visto = set()
    nodes = [inicio] + sorted(g.keys()) if inicio and inicio in g else sorted(g.keys())

    for v in nodes:
        if v in visto:
            continue
        q = deque([v])
        visto.add(v)
        dist = {v: 0}
        ordem = []
        while q:
            u = q.popleft()
            ordem.append(u)
            for nb in sorted(g.get(u, [])):
                if nb not in visto:
                    visto.add(nb)
                    dist[nb] = dist[u] + 1
                    q.append(nb)
        if ordem:
            componentes.append(f"[{','.join(f'{x}={dist.get(x,0)}' for x in ordem)}]")

    return componentes


if __name__ == '__main__':
    grafo = {
        'A': ['J', 'F', 'D', 'E'],
        'J': ['A', 'F'],
        'F': ['A', 'J', 'E'],
        'D': ['A', 'E'],
        'E': ['A', 'F', 'D', 'B', 'C'],
        'B': ['E', 'C'],
        'C': ['E', 'B'],
        'G': ['H', 'I'],
        'H': ['G', 'I'],
        'I': ['G', 'H'],
    }
    resultado = BFS(grafo, direcionado=False, inicio='B')
    for r in resultado:
        print(r)