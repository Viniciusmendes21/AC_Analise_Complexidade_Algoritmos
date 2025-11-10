from collections import deque, defaultdict


def BFS(arestas, direcionado=False, inicio=None):
    if isinstance(arestas, dict):
        g = {}
        for k, vs in arestas.items():
            key = str(k).strip()
            g.setdefault(key, [])
            for v in vs:
                if v is None:
                    continue
                nb = str(v).strip()
                if nb:
                    g[key].append(nb)
        if not direcionado:
            for u, nbrs in list(g.items()):
                for v in nbrs:
                    g.setdefault(v, [])
                    if u not in g[v]:
                        g[v].append(u)
    else:
        g = defaultdict(list)
        tokens = [t.strip() for t in arestas.split(',')] if isinstance(arestas, str) else list(arestas)

        for tok in tokens:
            if isinstance(tok, (list, tuple)) and len(tok) >= 2:
                a, b = str(tok[0]).strip(), str(tok[1]).strip()
            else:
                s = str(tok).strip()
                if not s:
                    continue
                if '-' in s:
                    a, b = (p.strip() for p in s.split('-', 1))
                else:
                    if len(s) > 1:
                        raise ValueError(f"Token inválido: '{s}'. Use vértice único (ex.: 'G') ou arestas explícitas (ex.: 'G-H,G-I').")
                    g.setdefault(s, [])
                    continue

            if not a or not b:
                continue

            if a == b:
                # self-loop
                g.setdefault(a, []).append(b)
                if not direcionado:
                    g.setdefault(a, []).append(b)
            else:
                g.setdefault(a, []).append(b)
                if not direcionado:
                    g.setdefault(b, []).append(a)

        g = dict(g)

    componentes = []
    visto = set()

    # BFS inlined (antes função auxiliar)
    if inicio and inicio in g:
        q = deque([inicio])
        visto.add(inicio)
        distc = {inicio: 0}
        ordem = []
        while q:
            u = q.popleft()
            ordem.append(u)
            for nb in sorted(g.get(u, [])):
                if nb not in visto:
                    visto.add(nb)
                    distc[nb] = distc[u] + 1
                    q.append(nb)
        if ordem:
            componentes.append(f"[{','.join(f'{x}={distc.get(x,0)}' for x in ordem)}]")

    for v in sorted(g.keys()):
        if v in visto:
            continue
        q = deque([v])
        visto.add(v)
        distc = {v: 0}
        ordem = []
        while q:
            u = q.popleft()
            ordem.append(u)
            for nb in sorted(g.get(u, [])):
                if nb not in visto:
                    visto.add(nb)
                    distc[nb] = distc[u] + 1
                    q.append(nb)
        if ordem:
            componentes.append(f"[{','.join(f'{x}={distc.get(x,0)}' for x in ordem)}]")

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