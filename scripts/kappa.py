#!/usr/bin/env python3
"""Kappa de Cohen entre dois revisores a partir de um CSV com colunas id, revisor_a, revisor_b (valores 1 = incluir, 0 = excluir).
Uso: python3 kappa.py triagem_dupla.csv"""
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
a = [int(r["revisor_a"]) for r in rows]; b = [int(r["revisor_b"]) for r in rows]; n = len(rows)
tab = {(i, j): sum(1 for x, y in zip(a, b) if x == i and y == j) for i in (1, 0) for j in (1, 0)}
po = (tab[1, 1] + tab[0, 0]) / n
pa1, pb1 = sum(a) / n, sum(b) / n
pe = pa1 * pb1 + (1 - pa1) * (1 - pb1)
k = (po - pe) / (1 - pe)
faixa = ("quase perfeita" if k > .80 else "substancial" if k > .60 else "moderada" if k > .40 else "razoável" if k > .20 else "leve" if k > 0 else "pobre")
print(f"n = {n}")
print(f"              B: incluir  B: excluir")
print(f"A: incluir      {tab[1,1]:>5}       {tab[1,0]:>5}")
print(f"A: excluir      {tab[0,1]:>5}       {tab[0,0]:>5}")
print(f"po = {po:.3f}   pe = {pe:.3f}   kappa = {k:.3f}  ({faixa}, Landis e Koch 1977)")
print(f"discordâncias a resolver por consenso: {tab[1,0] + tab[0,1]}")
