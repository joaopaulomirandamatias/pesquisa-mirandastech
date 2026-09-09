#!/usr/bin/env python3
r"""Resume a codificação feita no Taguette: frequência de cada etiqueta (tag) por documento e coocorrência entre etiquetas.

    python3 scripts/codificar_taguette.py destaques.csv [--codebook codebook.csv] [--markdown sintese.md]

Entrada: o CSV exportado no Taguette em «Export highlights» (colunas id, document, tag, content) e, opcionalmente, o
codebook exportado («Export codebook» em CSV: tag, description, number of highlights). Saída: tabela etiqueta × documento
com contagens, total por etiqueta, trechos por etiqueta (os três mais curtos, para conferir) e coocorrência (dois trechos
iguais com etiquetas diferentes). Não interpreta: a leitura dos temas é do pesquisador (Braun & Clarke, 2006).
"""
import argparse, csv, itertools, sys
from collections import Counter, defaultdict

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("destaques"); ap.add_argument("--codebook"); ap.add_argument("--markdown")
    a = ap.parse_args()
    linhas = list(csv.DictReader(open(a.destaques, encoding="utf-8")))
    if not linhas: sys.exit("CSV vazio")
    cols = {c.lower(): c for c in linhas[0].keys()}
    cdoc = cols.get("document") or cols.get("documento"); ctag = cols.get("tag") or cols.get("etiqueta"); ctxt = cols.get("content") or cols.get("trecho") or cols.get("text")
    if not (cdoc and ctag and ctxt): sys.exit(f"colunas esperadas document, tag, content; achei {list(linhas[0].keys())}")
    # o Taguette lista várias tags separadas por ; num mesmo destaque
    regs = []
    for l in linhas:
        for t in [x.strip() for x in l[ctag].split(";") if x.strip()]: regs.append((l[cdoc], t, l[ctxt].strip()))
    docs = sorted({d for d, _, _ in regs}); tags = Counter(t for _, t, _ in regs)
    matriz = defaultdict(Counter)
    for d, t, _ in regs: matriz[t][d] += 1
    desc = {}
    if a.codebook:
        for l in csv.DictReader(open(a.codebook, encoding="utf-8")):
            k = {c.lower(): v for c, v in l.items()}; desc[k.get("tag", "")] = k.get("description", "")
    out = [f"# Codificação: {len(linhas)} destaques, {len(tags)} etiquetas, {len(docs)} documentos\n", "| Etiqueta | " + " | ".join(docs) + " | Total | Descrição |", "|---|" + "---|" * (len(docs) + 2)]
    for t, n in tags.most_common(): out.append(f"| {t} | " + " | ".join(str(matriz[t][d]) for d in docs) + f" | {n} | {desc.get(t, '')} |")
    out.append("\n## Trechos por etiqueta (os três mais curtos, para conferir a aplicação do código)")
    for t, _ in tags.most_common():
        trechos = sorted({x for _, tt, x in regs if tt == t}, key=len)[:3]
        out.append(f"\n**{t}**"); out += [f"- «{x[:160]}{'…' if len(x) > 160 else ''}»" for x in trechos]
    co = Counter()
    por_trecho = defaultdict(set)
    for d, t, x in regs: por_trecho[(d, x)].add(t)
    for ts in por_trecho.values():
        for p in itertools.combinations(sorted(ts), 2): co[p] += 1
    if co:
        out.append("\n## Coocorrência (mesmo trecho com duas etiquetas)")
        out += [f"- {p[0]} × {p[1]}: {n}" for p, n in co.most_common(10)]
    texto = "\n".join(out); print(texto)
    if a.markdown: open(a.markdown, "w", encoding="utf-8").write(texto + "\n"); print(f"\ngravado: {a.markdown}")

if __name__ == "__main__": main()
