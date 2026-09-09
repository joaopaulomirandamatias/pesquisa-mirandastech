#!/usr/bin/env python3
"""Deduplica registros exportados de bases (CSV/RIS convertido) por DOI e por título normalizado.
Uso: python3 deduplicar.py entrada.csv saida.csv
Colunas esperadas: title, doi (as demais são preservadas). Gera também saida_duplicatas.csv com o que foi removido."""
import csv, re, sys, unicodedata
def norm(t):
    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()
ent, sai = sys.argv[1], sys.argv[2]
linhas = list(csv.DictReader(open(ent, encoding="utf-8")))
vistos_doi, vistos_tit, unicos, dup = set(), set(), [], []
for r in linhas:
    doi = (r.get("doi") or "").lower().replace("https://doi.org/", "").strip()
    tit = norm(r.get("title"))
    if (doi and doi in vistos_doi) or (tit and tit in vistos_tit):
        r["motivo"] = "doi repetido" if doi and doi in vistos_doi else "título repetido"; dup.append(r); continue
    if doi: vistos_doi.add(doi)
    if tit: vistos_tit.add(tit)
    unicos.append(r)
campos = list(linhas[0].keys())
csv.DictWriter(open(sai, "w", encoding="utf-8", newline=""), fieldnames=campos).writeheader() or None
with open(sai, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=campos); w.writeheader(); w.writerows(unicos)
with open(sai.replace(".csv", "_duplicatas.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=campos + ["motivo"]); w.writeheader(); w.writerows(dup)
print(f"lidos {len(linhas)} · únicos {len(unicos)} · duplicatas removidas {len(dup)}")
