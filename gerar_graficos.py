import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configuração visual limpa para publicação/relatório acadêmico
plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "legend.fontsize": 9.5,
    "figure.dpi": 300,
    "axes.grid": True,
    "grid.linestyle": "--",
    "grid.alpha": 0.45,
})

CORES = {
    "C99_2col": "#1f77b4",
    "Py_2col": "#17becf",
    "C99_3col": "#d62728",
    "Py_3col": "#ff7f0e",
    "melhor": "#2ca02c",
    "medio": "#1f77b4",
    "pior": "#d62728",
}

def carregar_dados(caminho="resultados/benchmark.csv"):
    df = pd.read_csv(caminho)
    df = df[df["status"] == "OK"].copy()
    df["V"] = df["V"].astype(int)
    df["E"] = df["E"].astype(int)
    df["media_s"] = df["media_s"].astype(float)
    df["desvio_s"] = df["desvio_s"].astype(float)
    return df

def plot_1_contraste_p_vs_np(df, pasta_saida):
    """Gráfico 1: Contraste direto P vs NP (V = 10 a 34, pior caso)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

    sub_2c_c = df[(df["algoritmo"] == "2-Coloracao (Contraste)") & (df["linguagem"] == "C99") & (df["caso"] == "pior")].sort_values("V")
    sub_2c_p = df[(df["algoritmo"] == "2-Coloracao (Contraste)") & (df["linguagem"] == "Python") & (df["caso"] == "pior")].sort_values("V")
    sub_3c_c = df[(df["algoritmo"] == "3-Coloracao (Backtracking)") & (df["linguagem"] == "C99") & (df["caso"] == "pior")].sort_values("V")
    sub_3c_p = df[(df["algoritmo"] == "3-Coloracao (Backtracking)") & (df["linguagem"] == "Python") & (df["caso"] == "pior")].sort_values("V")

    # Painel A: Escala Linear (mostra a explosão vertical do NP-completo vs P colado no zero)
    ax1.errorbar(sub_2c_c["V"], sub_2c_c["media_s"], yerr=sub_2c_c["desvio_s"], fmt="o-", color=CORES["C99_2col"], label="2-Col BFS (C99) — P", capsize=3)
    ax1.errorbar(sub_2c_p["V"], sub_2c_p["media_s"], yerr=sub_2c_p["desvio_s"], fmt="s--", color=CORES["Py_2col"], label="2-Col BFS (Python) — P", capsize=3)
    ax1.errorbar(sub_3c_c["V"], sub_3c_c["media_s"], yerr=sub_3c_c["desvio_s"], fmt="^-", color=CORES["C99_3col"], label="3-Col Backtrack (C99) — NP-Completo", capsize=3)
    ax1.errorbar(sub_3c_p["V"], sub_3c_p["media_s"], yerr=sub_3c_p["desvio_s"], fmt="D-", color=CORES["Py_3col"], label="3-Col Backtrack (Python) — NP-Completo", capsize=3)

    ax1.axhline(60.0, color="black", linestyle=":", linewidth=1.3, label="Limite operacional (60 s)")
    ax1.set_title("(a) Escala Linear — Explosão Exponencial")
    ax1.set_xlabel("Número de Vértices (V)")
    ax1.set_ylabel("Tempo Médio de Execução (s)")
    ax1.set_ylim(-1, 65)
    ax1.legend(loc="upper left")

    # Painel B: Escala Semi-Log (permite enxergar as 4 curvas simultaneamente)
    ax2.errorbar(sub_2c_c["V"], sub_2c_c["media_s"], yerr=sub_2c_c["desvio_s"], fmt="o-", color=CORES["C99_2col"], label="2-Col BFS (C99)", capsize=3)
    ax2.errorbar(sub_2c_p["V"], sub_2c_p["media_s"], yerr=sub_2c_p["desvio_s"], fmt="s--", color=CORES["Py_2col"], label="2-Col BFS (Python)", capsize=3)
    ax2.errorbar(sub_3c_c["V"], sub_3c_c["media_s"], yerr=sub_3c_c["desvio_s"], fmt="^-", color=CORES["C99_3col"], label="3-Col Backtrack (C99)", capsize=3)
    ax2.errorbar(sub_3c_p["V"], sub_3c_p["media_s"], yerr=sub_3c_p["desvio_s"], fmt="D-", color=CORES["Py_3col"], label="3-Col Backtrack (Python)", capsize=3)

    ax2.axhline(60.0, color="black", linestyle=":", linewidth=1.3, label="Corte de 60 s")
    ax2.set_yscale("log")
    ax2.set_title("(b) Escala Semi-Log — Separação de Ordens de Grandeza")
    ax2.set_xlabel("Número de Vértices (V)")
    ax2.set_ylabel("Tempo Médio de Execução (s) [escala log]")
    ax2.legend(loc="upper left")

    fig.suptitle("Contraste Empírico P × NP: 2-Coloração (BFS) vs. 3-Coloração (Backtracking) — Pior Caso", fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_saida, "1_contraste_P_vs_NP.png"), bbox_inches="tight")
    plt.close()

def plot_2_linguagens(df, pasta_saida):
    """Gráfico 2: Comparação Linguagem x Linguagem (C99 -O2 vs Python)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

    # Painel A: 2-Coloração BFS (pior caso, escala log-log)
    bfs_c = df[(df["algoritmo"] == "2-Coloracao (BFS)") & (df["linguagem"] == "C99") & (df["caso"] == "pior")].sort_values("V")
    bfs_p = df[(df["algoritmo"] == "2-Coloracao (BFS)") & (df["linguagem"] == "Python") & (df["caso"] == "pior")].sort_values("V")

    ax1.errorbar(bfs_c["V"], bfs_c["media_s"], yerr=bfs_c["desvio_s"], fmt="o-", color=CORES["C99_2col"], label="C99 (-O2)", capsize=3)
    ax1.errorbar(bfs_p["V"], bfs_p["media_s"], yerr=bfs_p["desvio_s"], fmt="s-", color=CORES["Py_2col"], label="Python 3", capsize=3)
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_title("(a) 2-Coloração BFS (Pior Caso — Escala Log-Log)")
    ax1.set_xlabel("Número de Vértices (V) [escala log]")
    ax1.set_ylabel("Tempo Médio (s) [escala log]")
    ax1.legend(loc="upper left")

    # Anota speedup no maior ponto (V=300.000)
    speedup_bfs = bfs_p["media_s"].iloc[-1] / bfs_c["media_s"].iloc[-1]
    ax1.annotate(f"Speedup (V=300k): {speedup_bfs:.1f}x",
                 xy=(bfs_c["V"].iloc[-1], bfs_c["media_s"].iloc[-1]),
                 xytext=(35000, 0.015),
                 arrowprops=dict(arrowstyle="->", color="gray"),
                 fontsize=9.5, fontweight="bold")

    # Painel B: 3-Coloração Backtracking (caso médio na transição de fase c=4.69, semi-log)
    bt_c = df[(df["algoritmo"] == "3-Coloracao (Backtracking)") & (df["linguagem"] == "C99") & (df["caso"] == "medio")].sort_values("V")
    bt_p = df[(df["algoritmo"] == "3-Coloracao (Backtracking)") & (df["linguagem"] == "Python") & (df["caso"] == "medio")].sort_values("V")

    ax2.errorbar(bt_c["V"], bt_c["media_s"], yerr=bt_c["desvio_s"], fmt="^-", color=CORES["C99_3col"], label="C99 (-O2)", capsize=3)
    ax2.errorbar(bt_p["V"], bt_p["media_s"], yerr=bt_p["desvio_s"], fmt="D-", color=CORES["Py_3col"], label="Python 3", capsize=3)
    ax2.set_yscale("log")
    ax2.set_title("(b) 3-Coloração Backtracking (Caso Médio c=4,69 — Semi-Log)")
    ax2.set_xlabel("Número de Vértices (V)")
    ax2.set_ylabel("Tempo Médio (s) [escala log]")
    ax2.legend(loc="upper left")

    speedup_bt = bt_p["media_s"].iloc[-1] / bt_c["media_s"].iloc[-1]
    ax2.annotate(f"Speedup (V=34): {speedup_bt:.1f}x",
                 xy=(bt_c["V"].iloc[-1], bt_c["media_s"].iloc[-1]),
                 xytext=(21, 0.004),
                 arrowprops=dict(arrowstyle="->", color="gray"),
                 fontsize=9.5, fontweight="bold")

    fig.suptitle("Comparação entre Linguagens: C99 (-O2) vs. Python 3", fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_saida, "2_linguagem_C99_vs_Python.png"), bbox_inches="tight")
    plt.close()

def plot_3_casos_forcados(df, pasta_saida):
    """Gráfico 3: Melhor caso, Caso médio e Pior caso para ambos os algoritmos (C99)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

    for caso, label, fmt in [("melhor", "Melhor Caso (K3 inicial — Ω(1))", "o-"),
                             ("medio", "Caso Médio (Erdős-Rényi)", "s--"),
                             ("pior", "Pior Caso (Bipartido conexo — Θ(V+E))", "^-")]:
        sub = df[(df["algoritmo"] == "2-Coloracao (BFS)") & (df["linguagem"] == "C99") & (df["caso"] == caso)].sort_values("V")
        ax1.errorbar(sub["V"], sub["media_s"], yerr=sub["desvio_s"], fmt=fmt, color=CORES[caso], label=label, capsize=3)

    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_title("(a) 2-Coloração (BFS) em C99 — Impacto da Entrada")
    ax1.set_xlabel("Número de Vértices (V) [escala log]")
    ax1.set_ylabel("Tempo Médio (s) [escala log]")
    ax1.legend(loc="upper left")

    for caso, label, fmt in [("melhor", "Melhor Caso (Grafo caminho — Ω(V))", "o-"),
                             ("medio", "Caso Médio (Transição fase c=4,69)", "s--"),
                             ("pior", "Pior Caso (Subgrafo + K4 — O(3^V))", "^-")]:
        sub = df[(df["algoritmo"] == "3-Coloracao (Backtracking)") & (df["linguagem"] == "C99") & (df["caso"] == caso)].sort_values("V")
        ax2.errorbar(sub["V"], sub["media_s"], yerr=sub["desvio_s"], fmt=fmt, color=CORES[caso], label=label, capsize=3)

    ax2.set_yscale("log")
    ax2.set_title("(b) 3-Coloração (Backtracking) em C99 — Impacto da Entrada")
    ax2.set_xlabel("Número de Vértices (V)")
    ax2.set_ylabel("Tempo Médio (s) [escala log]")
    ax2.legend(loc="upper left")

    fig.suptitle("Análise de Casos Forçados: Melhor Caso, Caso Médio e Pior Caso (C99)", fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_saida, "3_casos_forcados.png"), bbox_inches="tight")
    plt.close()

def plot_4_teorico_vs_medido(df, pasta_saida):
    """Gráfico 4: Validação Teórico vs. Medido (Razão T(n)/f(n) e Ajuste Exponencial)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

    # Painel A: Razão T(V, E) / (V + E) para o pior caso da BFS (deve tender a constante)
    for lang, cor, fmt in [("C99", CORES["C99_2col"], "o-"), ("Python", CORES["Py_2col"], "s-")]:
        sub = df[(df["algoritmo"] == "2-Coloracao (BFS)") & (df["linguagem"] == lang) & (df["caso"] == "pior")].sort_values("V").copy()
        sub["razao_ns"] = (sub["media_s"] / (sub["V"] + sub["E"])) * 1e9  # em nanossegundos por (V+E)
        ax1.plot(sub["V"], sub["razao_ns"], fmt, color=cor, label=f"{lang}: T(V,E) / (V + E)")

    ax1.set_xscale("log")
    ax1.set_title("(a) BFS Pior Caso: Razão Assintótica T(V,E) / (V + E)")
    ax1.set_xlabel("Número de Vértices (V) [escala log]")
    ax1.set_ylabel("Tempo Normalizado [ns / (V + E)]")
    ax1.legend(loc="best")

    # Painel B: Regressão exponencial nos picos do pior caso da 3-Coloração (C99)
    sub_3c = df[(df["algoritmo"] == "3-Coloracao (Backtracking)") & (df["linguagem"] == "C99") & (df["caso"] == "pior")].sort_values("V")
    # Filtra os picos de pior caso (excluindo V=28 e V=32 que tiveram poda antecipada densa)
    picos = sub_3c[~sub_3c["V"].isin([28, 32])]

    ax2.scatter(sub_3c["V"], sub_3c["media_s"], color="gray", alpha=0.65, label="Todas as instâncias pior caso (C99)")
    ax2.plot(picos["V"], picos["media_s"], "o-", color=CORES["C99_3col"], label="Envoltória de pior caso efetivo")

    # Ajuste linear em log(T) = a*V + b => T(V) = c * base^V
    coef = np.polyfit(picos["V"], np.log(picos["media_s"]), 1)
    base_empirica = np.exp(coef[0])
    v_fit = np.linspace(10, 36, 100)
    t_fit = np.exp(coef[1]) * (base_empirica ** v_fit)
    ax2.plot(v_fit, t_fit, "--", color="black", label=f"Ajuste exponencial: O({base_empirica:.2f}^V)")

    ax2.set_yscale("log")
    ax2.set_title("(b) Backtracking Pior Caso: Ajuste Exponencial vs. Medido")
    ax2.set_xlabel("Número de Vértices (V)")
    ax2.set_ylabel("Tempo Médio (s) [escala log]")
    ax2.legend(loc="upper left")

    fig.suptitle("Validação Teórico × Medido: Convergência Linear Θ(V+E) e Crescimento Exponencial", fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_saida, "4_teorico_vs_medido.png"), bbox_inches="tight")
    plt.close()

def main():
    pasta_saida = "graficos"
    os.makedirs(pasta_saida, exist_ok=True)
    df = carregar_dados("resultados/benchmark.csv")

    plot_1_contraste_p_vs_np(df, pasta_saida)
    plot_2_linguagens(df, pasta_saida)
    plot_3_casos_forcados(df, pasta_saida)
    plot_4_teorico_vs_medido(df, pasta_saida)

    print(f"4 gráficos gerados com sucesso em '{pasta_saida}/' (300 DPI)!")

if __name__ == "__main__":
    main()