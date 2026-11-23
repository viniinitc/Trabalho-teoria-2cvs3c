import csv
import os
import subprocess
import sys
import tracemalloc
import matplotlib.pyplot as plt
import pandas as pd

# Importa diretamente as funções já implementadas no seu python/coloracao.py
sys.path.insert(0, os.path.abspath("python"))
from coloracao import ler_grafo, dois_colorivel_bfs, tres_colorivel_backtracking

WRAPPER_C = "c99/_mem_probe.c"
BIN_MEM = "c99/_mem_probe.exe" if os.name == "nt" else "./c99/_mem_probe"

CODIGO_PROBE_C = r"""
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

typedef struct {
    int V;
    int E;
    int *head;
    int *to;
    int *next;
    int edge_count;
} Grafo;

Grafo* criar_grafo(int V, int E) {
    Grafo *g = (Grafo*)malloc(sizeof(Grafo));
    g->V = V;
    g->E = E;
    g->head = (int*)malloc((size_t)V * sizeof(int));
    g->to = (int*)malloc((size_t)(2 * E + 1) * sizeof(int));
    g->next = (int*)malloc((size_t)(2 * E + 1) * sizeof(int));
    for (int i = 0; i < V; i++) g->head[i] = -1;
    g->edge_count = 0;
    return g;
}

void adicionar_aresta(Grafo *g, int u, int v) {
    g->to[g->edge_count] = v;
    g->next[g->edge_count] = g->head[u];
    g->head[u] = g->edge_count++;
    g->to[g->edge_count] = u;
    g->next[g->edge_count] = g->head[v];
    g->head[v] = g->edge_count++;
}

void liberar_grafo(Grafo *g) {
    free(g->head); free(g->to); free(g->next); free(g);
}

/* Mede pico de bytes auxiliares na BFS: vetor cor[V] + vetor fila[V] */
size_t pico_memoria_bfs(const Grafo *g) {
    size_t pico_bytes = 2 * (size_t)g->V * sizeof(int);
    int *cor = (int*)malloc((size_t)g->V * sizeof(int));
    int *fila = (int*)malloc((size_t)g->V * sizeof(int));
    for (int i = 0; i < g->V; i++) cor[i] = -1;

    bool ok = true;
    for (int inicio = 0; inicio < g->V && ok; inicio++) {
        if (cor[inicio] != -1) continue;
        int frente = 0, tras = 0;
        cor[inicio] = 0;
        fila[tras++] = inicio;
        while (frente < tras) {
            int u = fila[frente++];
            int prox = 1 - cor[u];
            for (int e = g->head[u]; e != -1; e = g->next[e]) {
                int v = g->to[e];
                if (cor[v] == -1) { cor[v] = prox; fila[tras++] = v; }
                else if (cor[v] == cor[u]) { ok = false; break; }
            }
            if (!ok) break;
        }
    }
    free(cor);
    free(fila);
    return pico_bytes;
}

static size_t max_profundidade = 0;

static bool bt_3col(const Grafo *g, int v, int *cor, size_t prof) {
    if (prof > max_profundidade) max_profundidade = prof;
    if (v == g->V) return true;
    for (int c = 0; c < 3; c++) {
        bool valido = true;
        for (int e = g->head[v]; e != -1; e = g->next[e]) {
            if (cor[g->to[e]] == c) { valido = false; break; }
        }
        if (valido) {
            cor[v] = c;
            if (bt_3col(g, v + 1, cor, prof + 1)) return true;
            cor[v] = -1;
        }
    }
    return false;
}

/* Mede pico de bytes auxiliares no Backtracking: vetor cor[V] + stack frames da recursão */
size_t pico_memoria_3col(const Grafo *g) {
    int *cor = (int*)malloc((size_t)g->V * sizeof(int));
    for (int i = 0; i < g->V; i++) cor[i] = -1;
    max_profundidade = 0;
    bt_3col(g, 0, cor, 1);
    free(cor);
    /* Heap: V * sizeof(int) + Stack: max_profundidade * ~48 bytes/frame x86_64 */
    return (size_t)g->V * sizeof(int) + max_profundidade * 48;
}

int main(int argc, char **argv) {
    if (argc < 3) return 1;
    FILE *f = fopen(argv[2], "r");
    if (!f) return 1;
    int V, E;
    if (fscanf(f, "%d %d", &V, &E) != 2) { fclose(f); return 1; }
    Grafo *g = criar_grafo(V, E);
    for (int i = 0; i < E; i++) {
        int u, v;
        if (fscanf(f, "%d %d", &u, &v) == 2) adicionar_aresta(g, u, v);
    }
    fclose(f);

    size_t pico = (strcmp(argv[1], "2col") == 0) ? pico_memoria_bfs(g) : pico_memoria_3col(g);
    printf("%zu\n", pico);
    liberar_grafo(g);
    return 0;
}
"""

def preparar_probe_c():
    with open(WRAPPER_C, "w", encoding="utf-8") as f:
        f.write(CODIGO_PROBE_C)
    subprocess.run(["gcc", "-std=c99", "-O2", WRAPPER_C, "-o", BIN_MEM], check=True)

def limpar_probe_c():
    for arq in [WRAPPER_C, BIN_MEM]:
        if os.path.exists(arq):
            os.remove(arq)

def medir_memoria_c(algoritmo, arquivo_grafo):
    out = subprocess.check_output([BIN_MEM, algoritmo, arquivo_grafo], text=True).strip()
    return int(out)

def medir_memoria_python(algoritmo, V, adj):
    tracemalloc.start()
    if algoritmo == "2col":
        dois_colorivel_bfs(V, adj)
    else:
        tres_colorivel_backtracking(V, adj)
    _, pico_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return pico_bytes

def gerar_grafico_memoria(df, caminho_png):
    plt.rcParams.update({
        "font.size": 11,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "figure.dpi": 300,
        "axes.grid": True,
        "grid.linestyle": "--",
        "grid.alpha": 0.45,
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

    # Painel A: 2-Coloração BFS (Escala Log-Log até V = 300.000)
    sub_2c = df[(df["algoritmo"] == "2-Coloracao (BFS)") & (df["caso"] == "pior")].sort_values("V")
    c_2c = sub_2c[sub_2c["linguagem"] == "C99"]
    p_2c = sub_2c[sub_2c["linguagem"] == "Python"]

    ax1.plot(c_2c["V"], c_2c["pico_kib"], "o-", color="#1f77b4", label="C99 (8 bytes/vértice)")
    ax1.plot(p_2c["V"], p_2c["pico_kib"], "s-", color="#17becf", label="Python (tracemalloc)")
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_title("(a) Espaço Auxiliar 2-Coloração BFS — Θ(V)")
    ax1.set_xlabel("Número de Vértices (V) [escala log]")
    ax1.set_ylabel("Pico de Memória Auxiliar (KiB) [escala log]")
    ax1.legend(loc="upper left")

    # Painel B: 3-Coloração Backtracking (Escala Linear V = 10 a 34 — prova que memória é O(V) mesmo quando tempo é O(3^V))
    sub_3c = df[(df["algoritmo"] == "3-Coloracao (Backtracking)") & (df["caso"] == "pior")].sort_values("V")
    c_3c = sub_3c[sub_3c["linguagem"] == "C99"]
    p_3c = sub_3c[sub_3c["linguagem"] == "Python"]

    ax2.plot(c_3c["V"], c_3c["pico_bytes"], "^-", color="#d62728", label="C99 (vetor cor + pilha)")
    ax2.plot(p_3c["V"], p_3c["pico_bytes"], "D-", color="#ff7f0e", label="Python (tracemalloc)")
    ax2.set_title("(b) Espaço Auxiliar 3-Coloração Backtracking — Θ(V)")
    ax2.set_xlabel("Número de Vértices (V)")
    ax2.set_ylabel("Pico de Memória Auxiliar (Bytes)")
    ax2.legend(loc="upper left")

    fig.suptitle("Análise Empírica de Complexidade de Espaço: Crescimento Linear Θ(V)", fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(caminho_png, bbox_inches="tight")
    plt.close()

def main():
    preparar_probe_c()
    os.makedirs("resultados", exist_ok=True)
    os.makedirs("graficos", exist_ok=True)

    registros = []
    try:
        # 1. Espaço da 2-Coloração (pior caso bipartido, V = 1.000 a 300.000)
        for n in [1000, 3000, 10000, 30000, 100000, 300000]:
            arq = f"entradas/2col_pior_{n}.txt"
            V, adj = ler_grafo(arq)
            mem_c = medir_memoria_c("2col", arq)
            mem_p = medir_memoria_python("2col", V, adj)
            registros.append(["2-Coloracao (BFS)", "C99", "pior", V, mem_c, round(mem_c / 1024, 3)])
            registros.append(["2-Coloracao (BFS)", "Python", "pior", V, mem_p, round(mem_p / 1024, 3)])

        # 2. Espaço da 3-Coloração (pior caso, V = 10 a 34 — note como leva milissegundos no V=34 se rodarmos só V<=30 ou V<=34)
        # Usa até V=30 para finalizar em < 10 segundos totais
        for n in [10, 14, 18, 22, 26, 28, 30]:
            arq = f"entradas/3col_pior_{n}.txt"
            V, adj = ler_grafo(arq)
            mem_c = medir_memoria_c("3col", arq)
            mem_p = medir_memoria_python("3col", V, adj)
            registros.append(["3-Coloracao (Backtracking)", "C99", "pior", V, mem_c, round(mem_c / 1024, 3)])
            registros.append(["3-Coloracao (Backtracking)", "Python", "pior", V, mem_p, round(mem_p / 1024, 3)])
    finally:
        limpar_probe_c()

    csv_path = "resultados/memoria.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["algoritmo", "linguagem", "caso", "V", "pico_bytes", "pico_kib"])
        writer.writerows(registros)

    df = pd.DataFrame(registros, columns=["algoritmo", "linguagem", "caso", "V", "pico_bytes", "pico_kib"])
    gerar_grafico_memoria(df, "graficos/5_complexidade_espaco.png")
    print(f"Medição de memória concluída!\n- Dados: {csv_path}\n- Gráfico: graficos/5_complexidade_espaco.png")

if __name__ == "__main__":
    main()