from collections import deque, defaultdict


def BFS(arestas, direcionado=False, inicio=None):
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

    def bfs_component(raiz):
        q = deque([raiz])
        visto.add(raiz)
        distc = {raiz: 0}
        ordem = []
        while q:
            u = q.popleft()
            ordem.append(u)
            for nb in sorted(g.get(u, [])):
                if nb not in visto:
                    visto.add(nb)
                    distc[nb] = distc[u] + 1
                    q.append(nb)
        return ordem, distc

    if inicio and inicio in g:
        ordem, distc = bfs_component(inicio)
        if ordem:
            componentes.append(f"[{','.join(f'{x}={distc.get(x,0)}' for x in ordem)}]")

    for v in sorted(g.keys()):
        if v in visto:
            continue
        ordem, distc = bfs_component(v)
        if ordem:
            componentes.append(f"[{','.join(f'{x}={distc.get(x,0)}' for x in ordem)}]")

    return componentes


if __name__ == '__main__':
    resultado = BFS('A-J, A-F, A-D, A-E, J-F, F-E, D-E, E-B, E-C, B-C, G-H, G-I, H-I', direcionado=False, inicio='B')
    for r in resultado:
        print(r)



