#define _POSIX_C_SOURCE 199309L
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#ifdef _WIN32
#include <windows.h>
double obter_tempo_segundos(void) {
    LARGE_INTEGER freq, contador;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&contador);
    return (double)contador.QuadPart / (double)freq.QuadPart;
}
#else
#include <time.h>
double obter_tempo_segundos(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec * 1e-9;
}
#endif

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
    free(g->head);
    free(g->to);
    free(g->next);
    free(g);
}

/* ALGORITMO A: 2-Coloração via BFS — O(V + E) */
bool dois_colorivel_bfs(const Grafo *g) {
    int V = g->V;
    int *cor = (int*)malloc((size_t)V * sizeof(int));
    int *fila = (int*)malloc((size_t)V * sizeof(int));
    for (int i = 0; i < V; i++) cor[i] = -1;

    bool resultado = true;

    for (int inicio = 0; inicio < V && resultado; inicio++) {
        if (cor[inicio] != -1) continue;

        int frente = 0, tras = 0;
        cor[inicio] = 0;
        fila[tras++] = inicio;

        while (frente < tras) {
            int u = fila[frente++];
            int proxima_cor = 1 - cor[u];

            for (int e = g->head[u]; e != -1; e = g->next[e]) {
                int v = g->to[e];
                if (cor[v] == -1) {
                    cor[v] = proxima_cor;
                    fila[tras++] = v;
                } else if (cor[v] == cor[u]) {
                    resultado = false;
                    break;
                }
            }
            if (!resultado) break;
        }
    }

    free(cor);
    free(fila);
    return resultado;
}

/* ALGORITMO B: 3-Coloração via Backtracking — O(3^V) */
static bool backtrack_3col(const Grafo *g, int v, int *cor) {
    if (v == g->V) return true;

    for (int c = 0; c < 3; c++) {
        bool valido = true;
        for (int e = g->head[v]; e != -1; e = g->next[e]) {
            int vizinho = g->to[e];
            if (cor[vizinho] == c) {
                valido = false;
                break;
            }
        }
        if (valido) {
            cor[v] = c;
            if (backtrack_3col(g, v + 1, cor)) return true;
            cor[v] = -1;
        }
    }
    return false;
}

bool tres_colorivel_backtracking(const Grafo *g) {
    int V = g->V;
    int *cor = (int*)malloc((size_t)V * sizeof(int));
    for (int i = 0; i < V; i++) cor[i] = -1;

    bool resultado = backtrack_3col(g, 0, cor);

    free(cor);
    return resultado;
}

int main(int argc, char **argv) {
    if (argc < 4) {
        fprintf(stderr, "Uso: %s <2col|3col> <arquivo_grafo> <repeticoes>\n", argv[0]);
        return 1;
    }

    const char *algoritmo = argv[1];
    const char *caminho = argv[2];
    int repeticoes = atoi(argv[3]);

    FILE *f = fopen(caminho, "r");
    if (!f) {
        perror("Erro ao abrir grafo");
        return 1;
    }

    int V, E;
    if (fscanf(f, "%d %d", &V, &E) != 2) {
        fclose(f);
        return 1;
    }

    Grafo *g = criar_grafo(V, E);
    for (int i = 0; i < E; i++) {
        int u, v;
        if (fscanf(f, "%d %d", &u, &v) == 2) {
            adicionar_aresta(g, u, v);
        }
    }
    fclose(f);

    /* Aquecimento (warm-up de cache) */
    bool res = false;
    if (strcmp(algoritmo, "2col") == 0) {
        res = dois_colorivel_bfs(g);
    } else if (strcmp(algoritmo, "3col") == 0) {
        res = tres_colorivel_backtracking(g);
    } else {
        fprintf(stderr, "Algoritmo invalido.\n");
        liberar_grafo(g);
        return 1;
    }

    /* Medição pura do algoritmo */
    printf("RESULTADO:%d\n", res ? 1 : 0);
    for (int r = 0; r < repeticoes; r++) {
        double t0 = obter_tempo_segundos();
        if (strcmp(algoritmo, "2col") == 0) {
            res = dois_colorivel_bfs(g);
        } else {
            res = tres_colorivel_backtracking(g);
        }
        double t1 = obter_tempo_segundos();
        printf("TEMPO:%.9f\n", t1 - t0);
    }

    liberar_grafo(g);
    return 0;
}