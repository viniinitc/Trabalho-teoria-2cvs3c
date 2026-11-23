import subprocess
import statistics
import csv
import os
import sys
from gerar_entradas import gerar_todas_instancias

REPETICOES = 20
TIMEOUT_SEGUNDOS = 60.0
BINARIO_C99 = "./c99/coloracao.exe" if os.name == "nt" else "./c99/coloracao"
SCRIPT_PY = "python/coloracao.py"

def compilar_c99():
    cmd = ["gcc", "-std=c99", "-O2", "-Wall", "-Wextra", "c99/coloracao.c", "-o", BINARIO_C99]
    subprocess.run(cmd, check=True)
    print("C99 compilado com sucesso (-std=c99 -O2).")

def executar_medicao(linguagem, algoritmo, arquivo_grafo, repeticoes=REPETICOES):
    if linguagem == "C99":
        cmd = [BINARIO_C99, algoritmo, arquivo_grafo, str(repeticoes)]
    else:
        cmd = [sys.executable, SCRIPT_PY, algoritmo, arquivo_grafo, str(repeticoes)]

    try:
        # Timeout cobre warm-up + todas as repetições; o limite de 60s é por execução individual
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SEGUNDOS * (repeticoes + 1),
            check=True
        )
    except subprocess.TimeoutExpired:
        return None, None, None, "TIMEOUT (>60s/exec)"

    resultado = None
    tempos = []
    for linha in proc.stdout.strip().splitlines():
        if linha.startswith("RESULTADO:"):
            resultado = int(linha.split(":")[1])
        elif linha.startswith("TEMPO:"):
            tempos.append(float(linha.split(":")[1]))

    media = statistics.mean(tempos)
    desvio = statistics.stdev(tempos) if len(tempos) > 1 else 0.0
    if media > TIMEOUT_SEGUNDOS:
        return None, None, None, "TIMEOUT (>60s/exec)"
    return resultado, media, desvio, "OK"


def rodar_testes_corretude():
    print("\n--- Executando Testes Automatizados de Corretude ---")
    tamanhos_teste = [10, 14, 18]
    casos = ["melhor", "medio", "pior"]

    for n in tamanhos_teste:
        for caso in casos:
            arq = f"entradas/3col_{caso}_{n}.txt"
            r_c_2, _, _, _ = executar_medicao("C99", "2col", arq, 1)
            r_p_2, _, _, _ = executar_medicao("Python", "2col", arq, 1)
            r_c_3, _, _, _ = executar_medicao("C99", "3col", arq, 1)
            r_p_3, _, _, _ = executar_medicao("Python", "3col", arq, 1)

            assert r_c_2 == r_p_2, f"Divergência 2-col em {arq}: C99={r_c_2}, Py={r_p_2}"
            assert r_c_3 == r_p_3, f"Divergência 3-col em {arq}: C99={r_c_3}, Py={r_p_3}"
            if r_c_2 == 1:
                assert r_c_3 == 1, f"Erro lógico: grafo 2-colorível deve ser 3-colorível ({arq})"

    print("TODOS OS TESTES DE CORRETUDE PASSARAM COM SUCESSO!\n")

def main():
    if not os.path.exists("entradas"):
        gerar_todas_instancias()

    compilar_c99()
    rodar_testes_corretude()

    os.makedirs("resultados", exist_ok=True)
    csv_path = "resultados/benchmark.csv"

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["algoritmo", "linguagem", "caso", "V", "E", "resultado", "media_s", "desvio_s", "status"])

        # 1. Benchmark 2-Coloração (escala polinomial)
        tamanhos_2col = [1000, 3000, 10000, 30000, 100000, 300000]
        for caso in ["melhor", "medio", "pior"]:
            for n in tamanhos_2col:
                arq = f"entradas/2col_{caso}_{n}.txt"
                with open(arq) as gf:
                    V, E = map(int, gf.readline().split())
                for lang in ["C99", "Python"]:
                    res, media, desvio, status = executar_medicao(lang, "2col", arq)
                    print(f"[2-Col | {lang:6s} | {caso:6s} | V={n:6d}] -> {status} ({media:.6f}s)" if media else f"[2-Col | {lang} | {caso} | V={n}] -> {status}")
                    writer.writerow(["2-Coloracao (BFS)", lang, caso, V, E, res, media, desvio, status])

        # 2. Benchmark 3-Coloração + 2-Coloração nas mesmas entradas pequenas (contraste P vs NP)
        tamanhos_3col = [10, 14, 18, 22, 26, 28, 30, 32, 34]
        for caso in ["melhor", "medio", "pior"]:
            estourou_60s = {"C99": False, "Python": False}

            for n in tamanhos_3col:
                arq = f"entradas/3col_{caso}_{n}.txt"
                with open(arq) as gf:
                    V, E = map(int, gf.readline().split())

                # Roda 2-Coloração nas mesmas entradas para comparação direta
                for lang in ["C99", "Python"]:
                    res, media, desvio, status = executar_medicao(lang, "2col", arq)
                    writer.writerow(["2-Coloracao (Contraste)", lang, caso, V, E, res, media, desvio, status])

                # Roda 3-Coloração (15 reps para V >= 26 para agilizar sem perder rigor estatístico)
                reps_3col = 15 if n >= 26 else REPETICOES
                for lang in ["C99", "Python"]:
                    if estourou_60s[lang]:
                        writer.writerow(["3-Coloracao (Backtracking)", lang, caso, V, E, None, None, None, "SKIPPED (>60s anterior)"])
                        continue

                    res, media, desvio, status = executar_medicao(lang, "3col", arq, reps_3col)
                    if status != "OK":
                        estourou_60s[lang] = True
                    print(f"[3-Col | {lang:6s} | {caso:6s} | V={n:2d}] -> {status}" + (f" ({media:.6f}s)" if media else ""))
                    writer.writerow(["3-Coloracao (Backtracking)", lang, caso, V, E, res, media, desvio, status])

    print(f"\nBenchmark finalizado! Resultados salvos em '{csv_path}'.")

if __name__ == "__main__":
    main()