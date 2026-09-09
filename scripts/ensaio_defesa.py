#!/usr/bin/env python3
r"""Cronômetro de ensaio da apresentação: marca o tempo de cada bloco enquanto você fala e compara com o previsto.

    python3 scripts/ensaio_defesa.py --minutos 30 [--blocos "Abertura;Contexto;Objetivos;Método;Resultados;Discussão;Conclusão"] [--previsto "10;15;5;20;30;10;10"] [--saida ensaio.csv]

Uso: pressione Enter ao terminar cada bloco; o script registra o tempo real, mostra a diferença para o previsto (em %) e, no fim, o total e os blocos que estouraram. Grava um CSV por ensaio para comparar ensaios sucessivos. Sem áudio, sem IA: só o relógio.
"""
import argparse, csv, datetime, time

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--minutos", type=float, required=True); ap.add_argument("--blocos", default="Abertura;Contexto;Objetivos;Método;Resultados;Discussão;Conclusão"); ap.add_argument("--previsto", default="10;15;5;20;30;10;10"); ap.add_argument("--saida", default=None); ap.add_argument("--simular", default=None, help="tempos reais em segundos separados por ; (para testes, sem esperar)")
    a = ap.parse_args(); blocos = a.blocos.split(";"); pct = [float(x) for x in a.previsto.split(";")]
    if len(blocos) != len(pct): raise SystemExit("blocos e previsto com tamanhos diferentes")
    prev = [a.minutos * 60 * p / sum(pct) for p in pct]; sim = [float(x) for x in a.simular.split(";")] if a.simular else None
    print(f"Ensaio de {a.minutos:g} min em {len(blocos)} blocos — Enter ao terminar cada bloco\n"); linhas = []; t0 = time.time(); tot = 0
    for i, (b, p) in enumerate(zip(blocos, prev)):
        if sim: real = sim[i]
        else:
            ini = time.time(); input(f"[{i+1}/{len(blocos)}] {b} (previsto {p/60:.1f} min) … "); real = time.time() - ini
        tot += real; dif = (real - p) / p * 100; marca = "ESTOUROU" if dif > 15 else ("curto" if dif < -30 else "ok")
        print(f"   {b:14} real {real/60:5.1f} min · previsto {p/60:5.1f} · {dif:+5.0f} %  {marca}"); linhas.append([b, f"{p/60:.2f}", f"{real/60:.2f}", f"{dif:+.0f}", marca])
    print(f"\nTotal: {tot/60:.1f} min de {a.minutos:g} previstos ({(tot/60 - a.minutos):+.1f} min)")
    if a.saida:
        with open(a.saida, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["data", "bloco", "previsto_min", "real_min", "dif_pct", "avaliacao"]); [w.writerow([datetime.datetime.now().isoformat(timespec="minutes")] + l) for l in linhas]
        print(f"gravado: {a.saida}")

if __name__ == "__main__": main()
