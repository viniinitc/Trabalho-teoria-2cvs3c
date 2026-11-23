import sys
import time
from collections import deque

def ler_grafo(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        linha_cabecalho = f.readline().split()
        V, E = int(linha_cabecalho[0]), int(linha_cabecalho[1])
        adj = [[] for _ in range(V)]
        for _ in range(E):
            u, v = map(int, f.readline().split())
            adj[u].append(v)
            adj[v].append(u)
    return V, adj

def dois_colorivel_bfs(V, adj):
    """ALGORITMO A: 2-Coloração via BFS — O(V + E)"""
    cor = [-1] * V
    for inicio in range(V):
        if cor[inicio] != -1:
            continue
        cor[inicio] = 0
        fila = deque([inicio])
        while fila:
            u = fila.popleft()
            proxima_cor = 1 - cor[u]
            for v in adj[u]:
                if cor[v] == -1:
                    cor[v] = proxima_cor
                    fila.append(v)
                elif cor[v] == cor[u]:
                    return False
    return True

def tres_colorivel_backtracking(V, adj):
    """ALGORITMO B: 3-Coloração via Backtracking — O(3^V)"""
    cor = [-1] * V

    def backtrack(v):
        if v == V:
            return True
        for c in range(3):
            valido = True
            for vizinho in adj[v]:
                if cor[vizinho] == c:
                    valido = False
                    break
            if valido:
                cor[v] = c
                if backtrack(v + 1):
                    return True
                cor[v] = -1
        return False

    return backtrack(0)

def main():
    if len(sys.argv) < 4:
        sys.stderr.write("Uso: python coloracao.py <2col|3col> <arquivo_grafo> <repeticoes>\n")
        sys.exit(1)

    algoritmo = sys.argv[1]
    caminho = sys.argv[2]
    repeticoes = int(sys.argv[3])

    V, adj = ler_grafo(caminho)

    # Aquecimento (warm-up)
    if algoritmo == "2col":
        res = dois_colorivel_bfs(V, adj)
    elif algoritmo == "3col":
        res = tres_colorivel_backtracking(V, adj)
    else:
        sys.exit(1)

    print(f"RESULTADO:{1 if res else 0}")
    for _ in range(repeticoes):
        t0 = time.perf_counter()
        if algoritmo == "2col":
            res = dois_colorivel_bfs(V, adj)
        else:
            res = tres_colorivel_backtracking(V, adj)
        t1 = time.perf_counter()
        print(f"TEMPO:{t1 - t0:.9f}")

if __name__ == "__main__":
    main()