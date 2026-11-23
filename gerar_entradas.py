import random
import os

SEED = 42

def salvar_grafo(caminho, num_vertices, arestas):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(f"{num_vertices} {len(arestas)}\n")
        for u, v in arestas:
            f.write(f"{u} {v}\n")

def gerar_melhor_caso_2col(n):
    """Triângulo K3 nos vértices (0, 1, 2) + vértices isolados: BFS aborta em O(1) após alocação."""
    arestas = [(0, 1), (1, 2), (0, 2)]
    return n, arestas

def gerar_pior_caso_2col(n, rng):
    """Grafo bipartido conexo denso (grade/bipartido esparsificado): força visita a todo V e E."""
    metade = n // 2
    arestas = set()
    # Garante conexidade em árvore bipartida
    for i in range(1, n):
        if i < metade:
            u = rng.randint(metade, n - 1)
        else:
            u = rng.randint(0, metade - 1)
        arestas.add((min(i, u), max(i, u)))
    # Adiciona arestas extras entre as duas partições (m ~ 3n)
    alvo_arestas = min(metade * (n - metade), 3 * n)
    while len(arestas) < alvo_arestas:
        u = rng.randint(0, metade - 1)
        v = rng.randint(metade, n - 1)
        arestas.add((u, v))
    return n, list(arestas)

def gerar_caso_medio_erdos_renyi(n, grau_medio, rng):
    """Grafo aleatório esparso G(n, M) equivalente a G(n, p) em O(M)."""
    num_arestas = min(n * (n - 1) // 2, int(round(n * grau_medio / 2.0)))
    arestas = set()
    while len(arestas) < num_arestas:
        u = rng.randint(0, n - 1)
        v = rng.randint(0, n - 1)
        if u != v:
            arestas.add((min(u, v), max(u, v)))
    return n, list(arestas)

def gerar_melhor_caso_3col(n):
    """Grafo caminho (0-1-2-...-n-1): 3-colorível sem nenhum retrocesso (backtrack = 0)."""
    arestas = [(i, i + 1) for i in range(n - 1)]
    return n, arestas

def gerar_pior_caso_3col(n, rng):
    """
    Grafo não 3-colorível difícil: subgrafo bipartido/3-colorível nos primeiros (n-4) vértices
    conectado a um clique K4 nos últimos 4 vértices, forçando explosão antes de detectar falha.
    """
    if n < 4:
        return n, [(i, j) for i in range(n) for j in range(i + 1, n)]
    arestas = set()
    limite = n - 4
    # Subgrafo 3-colorível na região inicial (grau médio ~ 4.5, zona de transição de fase)
    for u in range(limite):
        for v in range(u + 1, limite):
            if (u % 3) != (v % 3) and rng.random() < (4.7 / max(1, limite)):
                arestas.add((u, v))
    # Liga os vértices iniciais aos vértices do K4 final
    for u in range(limite):
        alvo = rng.randint(limite, n - 1)
        arestas.add((u, alvo))
    # Clique K4 nos últimos 4 vértices (impossível 3-colorir)
    for u in range(limite, n):
        for v in range(u + 1, n):
            arestas.add((u, v))
    return n, list(arestas)

def gerar_todas_instancias():
    rng = random.Random(SEED)
    
    # Escala polinomial para 2-Coloração (6 tamanhos em progressão geométrica)
    tamanhos_2col = [1000, 3000, 10000, 30000, 100000, 300000]
    for n in tamanhos_2col:
        salvar_grafo(f"entradas/2col_melhor_{n}.txt", *gerar_melhor_caso_2col(n))
        salvar_grafo(f"entradas/2col_medio_{n}.txt", *gerar_caso_medio_erdos_renyi(n, 4.0, rng))
        salvar_grafo(f"entradas/2col_pior_{n}.txt", *gerar_pior_caso_2col(n, rng))

    # Escala exponencial para 3-Coloração (10 a 34) + comparação direta com 2-Coloração
    tamanhos_3col = [10, 14, 18, 22, 26, 28, 30, 32, 34]
    for n in tamanhos_3col:
        salvar_grafo(f"entradas/3col_melhor_{n}.txt", *gerar_melhor_caso_3col(n))
        # Grau médio 4.69 = limiar crítico de transição de fase para 3-coloração
        salvar_grafo(f"entradas/3col_medio_{n}.txt", *gerar_caso_medio_erdos_renyi(n, 4.69, rng))
        salvar_grafo(f"entradas/3col_pior_{n}.txt", *gerar_pior_caso_3col(n, rng))

    print("Instâncias geradas com sucesso na pasta 'entradas/'.")

if __name__ == "__main__":
    gerar_todas_instancias()