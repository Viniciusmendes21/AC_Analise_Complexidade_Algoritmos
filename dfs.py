grafo = {
    'A': ['B', 'E'],
    'B': ['A', 'C', 'E'],
    'C': ['B', 'F'],
    'D': ['G', 'H'],
    'E': ['A', 'B', 'F'],
    'F': ['C', 'E', 'I'],
    'G': ['D', 'H'],
    'H': ['D', 'G'],
    'I': ['F']
}

grafo = {
    'A': ['B', 'F'],
    'B': ['C', 'E'],
    'C': ['D'],
    'D': ['B', 'H'],
    'E': ['D', 'G'],
    'F': ['E', 'G'],
    'G': ['F'],
    'H': ['G']
}

def dfs(grafo, partida, visitados=None, passo=1):
    visitados[partida] = {'PREVISIT': passo}
    passo += 1
    for ponto in grafo[partida]:
        if ponto not in visitados:
            passo = dfs(grafo, ponto, visitados, passo)[1]
    visitados[partida]['POSTVISIT'] = passo
    passo += 1
    return visitados, passo

def dfs_algo(grafo, partida):
    if partida not in grafo.keys():
        print("O início solicitado não faz parte do grafo passado")
        return False

    visitados = {}
    passo = 1
    
    visitados, passo = dfs(grafo, partida, visitados, passo)

    for vertice in grafo.keys():
        if vertice not in visitados:
            visitados, passo = dfs(grafo, vertice, visitados, passo)

    return visitados
    
        
print(dfs_algo(grafo, 'A'))