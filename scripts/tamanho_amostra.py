#!/usr/bin/env python3
"""Tamanho de amostra.

  proporção:  python3 tamanho_amostra.py proporcao --e 0.05 [--p 0.5] [--conf 0.95] [--N 1000]
  duas médias: python3 tamanho_amostra.py medias --d 0.5 [--alpha 0.05] [--poder 0.8]   (d de Cohen; n por grupo)
Fórmulas clássicas (Cochran; aproximação normal). Para desenhos complexos use G*Power ou o pacote pwr do R.
"""
import argparse, math
Z = {0.90: 1.645, 0.95: 1.960, 0.99: 2.576}
ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="tipo", required=True)
p1 = sub.add_parser("proporcao"); p1.add_argument("--e", type=float, required=True); p1.add_argument("--p", type=float, default=0.5); p1.add_argument("--conf", type=float, default=0.95); p1.add_argument("--N", type=int)
p2 = sub.add_parser("medias"); p2.add_argument("--d", type=float, required=True); p2.add_argument("--alpha", type=float, default=0.05); p2.add_argument("--poder", type=float, default=0.80)
a = ap.parse_args()
if a.tipo == "proporcao":
    z = Z[a.conf]; n0 = z*z*a.p*(1-a.p)/(a.e*a.e); n = n0/(1+(n0-1)/a.N) if a.N else n0
    print(f"n0 (população infinita) = {math.ceil(n0)}" + (f"; n ajustado para N={a.N} = {math.ceil(n)}" if a.N else "")); print(f"parâmetros: z={z}, p={a.p}, e={a.e}, confiança={a.conf}")
else:
    za = {0.05: 1.960, 0.01: 2.576, 0.10: 1.645}[a.alpha]; zb = {0.80: 0.842, 0.90: 1.282, 0.95: 1.645}[a.poder]
    n = 2*((za+zb)/a.d)**2; print(f"n por grupo ≈ {math.ceil(n)} (d={a.d}, α={a.alpha}, poder={a.poder}, bicaudal)")
