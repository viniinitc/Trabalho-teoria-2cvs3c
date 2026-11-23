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


Requisitos

    GCC com suporte a C99 (gcc --version)

    Python 3.10+ com as bibliotecas pandas, matplotlib e numpy

Bash

pip install pandas matplotlib numpy

Como Reproduzir os Resultados

    Clonar o repositório e acessar a pasta raiz:
    Bash

    git clone <URL_DO_SEU_REPOSITORIO>
    cd Trabalho-teoria-2cvs3c

    Gerar as instâncias de entrada (seed fixa = 42):
    Bash

    python gerar_entradas.py

    Compilar C99, validar testes automatizados de corretude e executar o benchmark:
    Bash

    python benchmark.py

    (Saída salva em resultados/benchmark.csv)

    Gerar os gráficos em alta resolução (300 DPI):
    Bash

    python gerar_graficos.py

    (Imagens salvas em graficos/)


---

### Checklist Final

<TemplateWidget component_placeholder_id="im_3ae6580a6a79676b" header_title="Plano de Execução — Entrega 24/11 (23:59h)" templateName="checklist">
```json
{
  "categories": ["Código e Experimentos", "Análise e Gráficos", "Relatório e Apresentação"],
  "items": [
    { "id": "1", "label": "Definir as 2 linguagens (C99 com -O2 e Python)", "category": "Código e Experimentos", "checked": true },
    { "id": "2", "label": "Criar gerador de grafos com seed fixa (gerar_entradas.py)", "category": "Código e Experimentos", "checked": true },
    { "id": "3", "label": "Implementar BFS (2-coloração) e Backtracking (3-coloração) nas 2 linguagens (coloracao.c e coloracao.py)", "category": "Código e Experimentos", "checked": true },
    { "id": "4", "label": "Rodar testes automatizados de corretude garantindo saída idêntica nas 4 versões", "category": "Código e Experimentos", "checked": true },
    { "id": "5", "label": "Executar benchmark (15-30 repetições, warm-up, corte de 60s) e salvar resultados/benchmark.csv", "category": "Análise e Gráficos", "checked": true },
    { "id": "6", "label": "Gerar gráficos (P vs NP, Linguagem vs Linguagem, Teórico vs Medido) e tabelas (média ± desvio-padrão)", "category": "Análise e Gráficos", "checked": true },
    { "id": "7", "label": "Redigir PDF único nos 7 tópicos + Specs do PC + Contribuições + Declaração de IA", "category": "Relatório e Apresentação", "checked": true },
    { "id": "8", "label": "Subir repositório limpo no GitHub com README reproduzível e preparar pitch de 7 min", "category": "Relatório e Apresentação", "checked": false }
  ]
}
