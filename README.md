# Análise de Complexidade Experimental: 2-Coloração (P) × 3-Coloração (NP-Completo)

Projeto desenvolvido para a disciplina de **Teoria da Computação / Teoria da Complexidade**, comparando o desempenho teórico e empírico de dois algoritmos de coloração de vértices em grafos implementados em **C99 (`-O2`)** e **Python 3**:

- **Algoritmo A (Classe P):** 2-Coloração de grafos via Busca em Largura (BFS) — $O(V + E)$
- **Algoritmo B (Classe NP-Completo):** 3-Coloração de grafos via Backtracking com poda — $O(3^V \cdot V)$

## Equipe

- **Arthur Martins**
- **Maria Clara Targino**
- **Nicole Brito**
- **Vinicius Tenorio**
- **Maria Emilia**

## Estrutura do Repositório

```text
├── c99/
│   └── coloracao.c          # Implementações em C99 com timer de alta precisão
├── python/
│   └── coloracao.py         # Implementações espelho em Python 3
├── gerar_entradas.py        # Gerador determinístico de grafos (SEED = 42)
├── benchmark.py             # Compilação, testes de corretude e benchmark (15–20 reps)
├── memoria.py               # Medição de memória auxiliar (tracemalloc / contabilização C99)
├── gerar_graficos.py        # Geração dos gráficos comparativos em 300 DPI
├── resultados/
│   ├── benchmark.csv        # Dados experimentais de tempo (média e desvio-padrão)
│   └── memoria.csv          # Dados experimentais de complexidade de espaço
└── graficos/                # Figuras geradas para o relatório técnico

Requisitos

    GCC com suporte ao padrão C99 (gcc --version)

    Python 3.10+ com as bibliotecas pandas, matplotlib e numpy

Bash

pip install pandas matplotlib numpy

Como Reproduzir os Resultados

    Clonar o repositório e acessar o diretório raiz:
    Bash

    git clone [https://github.com/viniinitc/Trabalho-teoria-2cvs3c.git](https://github.com/viniinitc/Trabalho-teoria-2cvs3c.git)
    cd Trabalho-teoria-2cvs3c

    Gerar as instâncias de entrada (semente aleatória fixa = 42):
    Bash

    python gerar_entradas.py

    (Cria os grafos de melhor caso, caso médio/transição de fase e pior caso na pasta entradas/.)

    Compilar C99, executar testes automatizados de corretude e rodar o benchmark de tempo:
    Bash

    python benchmark.py

    (Valida a equivalência entre as 4 implementações, realiza aquecimento, executa 15 a 20 repetições por instância com teto de 60 segundos e exporta os resultados para resultados/benchmark.csv.)

    Executar a análise de complexidade de espaço (bônus) e gerar todos os gráficos (300 DPI):
    Bash

    python memoria.py
    python gerar_graficos.py

    (Salva os dados de memória em resultados/memoria.csv e gera as 5 figuras comparativas na pasta graficos/.)
