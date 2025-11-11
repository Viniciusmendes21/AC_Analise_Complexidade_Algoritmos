import streamlit as st
import networkx as nx
import graphviz
import json
import time
from collections import deque
import os
import signal

# --- Importe suas funções originais ---
# (Certifique-se que BFS.py e dfs.py estão na mesma pasta)
from BFS import BFS as bfs_algo
from DFS import dfs_algo

# --- Exemplo de Grafo (para preencher a caixa de texto) ---
grafo_exemplo_dfs = {
    'A': ['B', 'F'], 'B': ['C', 'E'], 'C': ['D'],
    'D': ['B', 'H'], 'E': ['D', 'G'], 'F': ['E', 'G'],
    'G': ['F'], 'H': ['G']
}
grafo_exemplo_dfs_json = json.dumps(grafo_exemplo_dfs, indent=4)


# --- Configuração da Página ---
# Esta DEVE ser a PRIMEIRA chamada do Streamlit no seu script
st.set_page_config(layout="wide")


# --- BLOCO DO TÍTULO E BOTÃO DE SAIR ---

# 1. Injetamos o CSS para o botão vermelho
st.markdown(
    """
    <style>
    /* Estilo base do botão vermelho */
    div[data-testid="stButton"] > button {
        background-color: #FF4B4B; /* Cor vermelha (igual ao st.error) */
        color: white; /* Texto branco */
        border: none;
    }
    /* Efeito :hover (mouse por cima) */
    div[data-testid="stButton"] > button:hover {
        background-color: #E03C3C; /* Vermelho mais escuro */
        color: white;
        border: none;
    }
    
    /* Seletor MUITO específico para o nosso botão "Sair".
    Ele mira o botão que está dentro da TERCEIRA coluna do bloco horizontal.
    */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stVerticalBlock"]:nth-child(3) > div[data-testid="stButton"] > button {
        width: 100%; /* Faz o botão vermelho preencher a coluna */
    }
    
    /* Seletor para o botão "Executar" (para não ficar vermelho).
    Ele mira o botão dentro da primeira coluna (a de controles).
    */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stVerticalBlock"]:nth-child(1) > div[data-testid="stButton"] > button {
        background-color: #0068C9; /* Azul (cor padrão do Streamlit) */
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stVerticalBlock"]:nth-child(1) > div[data-testid="stButton"] > button:hover {
        background-color: #00509E; /* Azul escuro */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. Criamos as colunas para o layout do topo
col_titulo, col_espaco, col_botao = st.columns([0.65, 0.2, 0.15]) # (Título, Espaço Vazio, Botão)

with col_titulo:
    st.title("Visualizador de Algoritmos de Grafo")
    st.write("Insira o grafo (JSON), o nó inicial e execute o algoritmo para ver a visualização.")

# col_espaco fica vazia de propósito, para empurrar o botão

with col_botao:
    # 3. Criamos o botão "Sair"
    if st.button("Sair ❌"):
        st.info("Desligando o servidor... Você pode fechar esta aba.")
        time.sleep(1)
        # Envia o sinal de "morte" para o processo
        os.kill(os.getpid(), signal.SIGTERM)
# --- FIM DO BLOCO DO TÍTULO ---

def desenhar_grafo(g_nx, nos_na_estrutura, no_atual, nos_processados):
    """
    Cria um objeto Graphviz para desenhar o estado atual do grafo.
    - nos_na_estrutura: (Pilha do DFS ou Fila do BFS) - Fica azul
    - no_atual: (Sendo processado) - Fica vermelho
    - nos_processados: (Já concluídos) - Fica cinza
    """
    dot = graphviz.Digraph()
    dot.attr('node', shape='circle', style='filled')

    for no in g_nx.nodes():
        cor = "white" # Não visitado
        if no in nos_processados:
            cor = "#D3D3D3" # Cinza claro (visitado e finalizado)
        elif no in nos_na_estrutura:
            cor = "lightblue" # Azul (na pilha ou fila)
        
        if no == no_atual:
            cor = "#FF6B6B" # Vermelho (sendo processado agora)
            
        dot.node(no, label=no, fillcolor=cor, fontcolor="black")

    for u, v in g_nx.edges():
        dot.edge(u, v)
        
    return dot

def dfs_visual(g_nx, partida):
    """
    Um gerador que roda o DFS passo a passo, 'yield' o estado atual.
    """
    visitados = set()
    processados = set()
    pilha = [(partida, iter(g_nx[partida]))] # (nó, iterador dos vizinhos)
    
    visitados.add(partida)
    # nos_na_pilha, no_atual, nos_processados
    yield "visitando", partida, visitados.copy(), processados.copy()

    while pilha:
        no_pai, filhos = pilha[-1]
        
        try:
            no_filho = next(filhos)
            if no_filho not in visitados:
                visitados.add(no_filho)
                pilha.append((no_filho, iter(g_nx[no_filho])))
                yield "visitando", no_filho, visitados.copy(), processados.copy()
        
        except StopIteration:
            processados.add(no_pai)
            pilha.pop()
            yield "processado", no_pai, visitados.copy(), processados.copy()
            if pilha:
                yield "retornando", pilha[-1][0], visitados.copy(), processados.copy()
                
    yield "finalizado", None, visitados.copy(), processados.copy()

def bfs_visual(g_nx, partida):
    """
    Um gerador que roda o BFS passo a passo, 'yield' o estado atual.
    """
    fila = deque([partida])
    visitados_descobertos = set([partida]) # Todos os nós já vistos
    processados_concluidos = set()      # Nós cujos vizinhos já foram checados
    
    # status, no_atual, nos_na_fila, nos_processados
    yield "descobrindo", partida, set(fila), processados_concluidos.copy()

    while fila:
        no_atual = fila.popleft()
        
        yield "processando", no_atual, set(fila), processados_concluidos.copy()
        
        for vizinho in g_nx.neighbors(no_atual):
            if vizinho not in visitados_descobertos:
                visitados_descobertos.add(vizinho)
                fila.append(vizinho)
                yield "descobrindo", vizinho, set(fila), processados_concluidos.copy()
        
        processados_concluidos.add(no_atual)
        yield "finalizado", no_atual, set(fila), processados_concluidos.copy()
        
    yield "concluido", None, set(fila), processados_concluidos.copy()


# --- LAYOUT PRINCIPAL DA APLICAÇÃO ---

col_setup, col_viz = st.columns([1, 2]) # Coluna de setup (33%) e visualização (66%)

with col_setup:
    st.header("Controles")
    
    algo_escolhido = st.radio("Escolha o Algoritmo", ["DFS", "BFS"])
    
    json_grafo = st.text_area(
        "Grafo (JSON)", 
        value=grafo_exemplo_dfs_json, 
        height=300
    )
    
    partida = st.text_input("Nó de Partida", value="A")
    
    velocidade = st.slider("Velocidade da Animação (segundos por passo)", 0.1, 2.0, 0.75, 0.1)

    executar = st.button("Executar Visualização")

with col_viz:
    st.header("Visualização")
    # 'tela' é o nosso "quadro branco" que será redesenhado
    tela_visual = st.empty()
    
    st.header("Resultado Final (do seu script original)")
    # 'output_final' é onde o resultado do seu script original será mostrado
    output_final = st.empty()


# --- LÓGICA DE EXECUÇÃO ---

if executar:
    try:
        # 1. Preparar o Grafo (comum para ambos)
        grafo_dict = json.loads(json_grafo)
        G = nx.DiGraph() # Usar DiGraph para setas direcionadas
        for no, vizinhos in grafo_dict.items():
            G.add_node(no) # Garante que nós sem vizinhos sejam adicionados
            for vizinho in vizinhos:
                G.add_edge(no, vizinho)
        
        output_final.empty() # Limpa o resultado anterior

        # --- Execução do DFS ---
        if algo_escolhido == "DFS":
            for status, no_atual, nos_pilha, nos_processados in dfs_visual(G, partida):
                dot_graph = desenhar_grafo(G, nos_pilha, no_atual, nos_processados)
                tela_visual.graphviz_chart(dot_graph)
                
                if status == "finalizado":
                    tela_visual.success(f"Visualização DFS Concluída!")
                    break
                time.sleep(velocidade)

            # Rodar script original para comparar
            resultado_script_original = dfs_algo(grafo_dict, partida)
            output_final.json(resultado_script_original)
        
        # --- Execução do BFS ---
        elif algo_escolhido == "BFS":
            for status, no_atual, nos_fila, nos_processados in bfs_visual(G, partida):
                dot_graph = desenhar_grafo(G, nos_fila, no_atual, nos_processados)
                tela_visual.graphviz_chart(dot_graph)
                
                if status == "concluido":
                    tela_visual.success(f"Visualização BFS Concluída!")
                    break
                time.sleep(velocidade)
            
            # Rodar script original para comparar
            resultado_bfs = bfs_algo(
                grafo_dict, 
                direcionado=False, 
                inicio=partida
            )
            output_final.code("\n".join(resultado_bfs), language="text")

    except KeyError as e:
        st.error(f"Erro: O nó de partida '{e}' não foi encontrado no grafo. Verifique seu JSON ou o campo 'Nó de Partida'.")
    except json.JSONDecodeError:
        st.error("Erro no JSON. Verifique a sintaxe (ex: vírgulas, aspas duplas).")
    except Exception as e:
        st.error(f"Erro inesperado ao executar: {e}")