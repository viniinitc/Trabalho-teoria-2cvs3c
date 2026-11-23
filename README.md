# Análise de Complexidade Experimental: 2-Coloração (P) × 3-Coloração (NP-Completo)

Projeto desenvolvido para a disciplina de **Teoria da Computação / Teoria da Complexidade**, comparando o desempenho teórico e empírico de dois algoritmos de coloração de grafos implementados em **C99 (`-O2`)** e **Python 3**:

- **Algoritmo A (Classe P):** 2-Coloração de grafos via Busca em Largura (BFS) — $O(V + E)$
- **Algoritmo B (Classe NP-Completo):** 3-Coloração de grafos via Backtracking com poda — $O(3^V)$

## Estrutura do Repositório

```text
├── c99/
│   └── coloracao.c          # Implementações em C99 com timer de alta precisão
├── python/
│   └── coloracao.py         # Implementações espelho em Python 3
├── gerar_entradas.py        # Gerador determinístico de grafos (SEED = 42)
├── benchmark.py             # Compilação, testes de corretude e benchmark (20 reps)
├── gerar_graficos.py        # Geração dos gráficos comparativos em 300 DPI
├── resultados/
│   └── benchmark.csv        # Dados experimentais coletados (média e desvio-padrão)
└── graficos/                # Figuras geradas para o relatório
