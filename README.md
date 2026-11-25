# Análise de Complexidade Experimental: 2-Coloração (P) × 3-Coloração (NP-completo)

Projeto da disciplina de **Teoria da Computação / Teoria da Complexidade**. Compara o desempenho teórico e experimental de dois algoritmos de coloração de vértices, cada um implementado em **C99 (`-O2`)** e em **Python 3**, ou seja, 4 implementações executadas sobre as mesmas entradas.

| Algoritmo | Problema | Classe | Complexidade de tempo |
|---|---|---|---|
| A: BFS | 2-Coloração | P | O(V + E) |
| B: Backtracking com poda | 3-Coloração | NP-completo | O(3^V · V) |

## Equipe

Arthur Martins, Maria Clara Targino, Nicole Brito, Vinícius Tenório e Maria Emília

## Estrutura do repositório

```text
├── c99/
│   └── coloracao.c          # Algoritmos A e B em C99, timer de alta precisão
├── python/
│   └── coloracao.py         # Algoritmos A e B em Python (espelho do C99)
├── gerar_entradas.py        # Gerador determinístico de grafos (SEED = 42)
├── benchmark.py             # Compilação, testes de corretude e medição de tempo
├── memoria.py               # Medição de memória auxiliar (bônus)
├── gerar_graficos.py        # Geração das 5 figuras (300 DPI)
├── entradas/                # Criada por gerar_entradas.py: grafos usados nos testes
├── resultados/
│   ├── benchmark.csv        # Tempos (média e desvio-padrão)
│   └── memoria.csv          # Memória auxiliar
└── graficos/                # Figuras usadas no relatório
```

## Ambiente de referência

Os resultados do relatório foram obtidos neste ambiente:

- **SO:** Windows 11 Home (64 bits)
- **CPU / RAM:** AMD64 Family 23 Model 104 (~1801 MHz), 32 GB
- **C:** GCC 16.2.0, `-std=c99 -O2`
- **Python:** CPython 3.14.10

## Requisitos

- GCC com suporte a C99 (`gcc --version`)
- Python 3.10 ou superior
- Bibliotecas Python: `pandas`, `matplotlib`, `numpy`

```bash
pip install pandas matplotlib numpy
```

## Como reproduzir os resultados

**1. Clonar o repositório**

```bash
git clone https://github.com/viniinitc/Trabalho-teoria-2cvs3c.git
cd Trabalho-teoria-2cvs3c
```

**2. Gerar as entradas** (semente fixa = 42)

```bash
python gerar_entradas.py
```

Cria na pasta `entradas/` os grafos de melhor caso, caso médio (grafos aleatórios G(n, M), com grau médio 4,0 na 2-Coloração e 4,69 na 3-Coloração, perto da transição de fase) e pior caso. Os quatro programas leem exatamente os mesmos arquivos. (O `benchmark.py` também gera as entradas sozinho se a pasta `entradas/` não existir.)

**3. Compilar, testar e medir o tempo**

```bash
python benchmark.py
```

O script realiza as seguintes etapas:

1. Compila o código C99 com `-std=c99 -O2` (mais `-Wall -Wextra`).
2. Roda os **testes de corretude** (`rodar_testes_corretude()`), que verificam se C99 e Python dão a mesma resposta (0 ou 1) nas instâncias de V = 10, 14 e 18 (melhor, médio e pior caso) e se todo grafo 2-colorível também é 3-colorível. Se alguma verificação falhar, o script é interrompido (`assert`) antes de qualquer medição.
3. Faz uma rodada de aquecimento (warm-up).
4. Mede **somente a execução do algoritmo**; leitura de arquivos e impressão ficam fora da medição.
5. Executa 20 repetições por instância (15 para V ≥ 26 na 3-Coloração) e calcula média e desvio-padrão.
6. Aplica um timeout ao lote de repetições e, se o tempo médio passar de 60 s, pula os tamanhos seguintes da 3-Coloração naquele caso e linguagem (marcados como `SKIPPED` no CSV).
7. Salva tudo em `resultados/benchmark.csv`.

> **Duração:** o 3-Coloração em Python leva até ~16 s por repetição nos maiores tamanhos, então o benchmark completo leva cerca de 10 minutos ou mais (varia conforme a máquina). Não é travamento.

**4. Medir memória (bônus) e gerar os gráficos**

```bash
python memoria.py
python gerar_graficos.py
```

`memoria.py` grava `resultados/memoria.csv` e também a figura `graficos/5_complexidade_espaco.png`. Ele precisa da pasta `entradas/` já criada (passo 2). `gerar_graficos.py` salva as figuras em `graficos/`.
