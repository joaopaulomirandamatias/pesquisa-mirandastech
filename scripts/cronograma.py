#!/usr/bin/env python3
"""Gera um cronograma (Gantt) em Markdown e SVG a partir de um CSV: atividade,inicio_mes,fim_mes,cor
    python3 scripts/cronograma.py 00_projeto/cronograma.csv --meses 12 --svg 00_projeto/cronograma.svg
"""
import argparse, csv
ap = argparse.ArgumentParser(); ap.add_argument("csv"); ap.add_argument("--meses", type=int, default=12); ap.add_argument("--svg")
a = ap.parse_args(); rows = list(csv.DictReader(open(a.csv, encoding="utf-8")))
print("| Atividade | " + " | ".join(str(m) for m in range(1, a.meses+1)) + " |"); print("|---|" + "---|"*a.meses)
for r in rows:
    i, f = int(r["inicio_mes"]), int(r["fim_mes"]); print(f"| {r['atividade']} | " + " | ".join("■" if i <= m <= f else " " for m in range(1, a.meses+1)) + " |")
if a.svg:
    cores = {"azul": "#17436B", "laranja": "#C4530E", "verde": "#186B50", "ambar": "#8A6000"}; W, L, H = 900, 200, 26
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{40+H*len(rows)}" font-family="sans-serif" font-size="12">']
    cw = (W-L-20)/a.meses
    for m in range(1, a.meses+1): s.append(f'<text x="{L+(m-0.5)*cw:.0f}" y="18" text-anchor="middle" fill="#555">{m}</text>')
    for k, r in enumerate(rows):
        y = 30+k*H; i, f = int(r["inicio_mes"]), int(r["fim_mes"])
        s.append(f'<text x="{L-8}" y="{y+16}" text-anchor="end">{r["atividade"]}</text><rect x="{L+(i-1)*cw:.0f}" y="{y+4}" width="{(f-i+1)*cw-2:.0f}" height="16" rx="2" fill="{cores.get(r.get("cor","azul"),"#17436B")}"/>')
    s.append("</svg>"); open(a.svg, "w", encoding="utf-8").write("\n".join(s)); print("svg:", a.svg)
