#!/usr/bin/env python3
r"""Indicadores descritivos de um corpus bibliográfico (CSV exportado do OpenAlex/Crossref/Scopus/WoS/Lens) — tabelas em Markdown e figura por script.

    python3 scripts/indicadores_bibliometricos.py corpus.csv [--citacoes crossref_refs.json] [--top 10] [--figura producao.png] [--markdown indicadores.md]

Colunas aceitas (nomes flexíveis): title, year, authors (separados por ; ou ,), source (periódico), doi, type, is_oa.
Produz: total, período, produção por ano (tabela e figura), periódicos mais frequentes, autores mais produtivos, tipos de documento,
proporção em acesso aberto e — se houver contagens de citações (arquivo JSON com doi e citacoes) — os mais citados e o índice h do corpus.
Não decide nada: indicadores descrevem o corpus da busca, não a «qualidade» de ninguém (Manifesto de Leiden; DORA).
"""
import argparse, csv, json, re
from collections import Counter

def col(r, *nomes):
    for n in nomes:
        for k in r:
            if k.lower().strip() == n: return r[k]
    return ""

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("corpus"); ap.add_argument("--citacoes"); ap.add_argument("--top", type=int, default=10); ap.add_argument("--figura"); ap.add_argument("--markdown")
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.corpus, encoding="utf-8")))
    anos = Counter(); fontes = Counter(); autores = Counter(); tipos = Counter(); oa = Counter(); n_aut = []
    for r in rows:
        y = re.search(r"\d{4}", col(r, "year", "publication_year", "ano") or ""); anos[int(y.group())] += 1 if y else 0
        s = col(r, "source", "journal", "container-title", "source title", "periodico"); fontes[s.strip()] += 1 if s.strip() else 0
        aut = [x.strip() for x in re.split(r";|\|", col(r, "authors", "author", "autores")) if x.strip()]; n_aut.append(len(aut))
        for x in aut: autores[x] += 1
        tipos[(col(r, "type", "tipo") or "?").strip()] += 1; oa[str(col(r, "is_oa", "oa")).strip().lower()] += 1
    md = [f"# Indicadores do corpus `{a.corpus}`", f"- Documentos: **{len(rows)}**; período: {min(anos)}–{max(anos)}; autores distintos: {len(autores)}; média de autores por documento: {sum(n_aut)/len(n_aut):.1f}".replace(".", ","),
          f"- Tipos: " + ", ".join(f"{k} {v}" for k, v in tipos.most_common()), f"- Acesso aberto (is_oa=true): {oa.get('true', 0)} de {len(rows)} ({oa.get('true', 0)/len(rows)*100:.0f} %)"]
    md += ["\n## Produção por ano", "| Ano | Documentos |", "|---|---|"] + [f"| {y} | {anos[y]} |" for y in sorted(anos)]
    md += [f"\n## Periódicos/fontes mais frequentes (top {a.top})", "| Fonte | Documentos |", "|---|---|"] + [f"| {k} | {v} |" for k, v in fontes.most_common(a.top)]
    md += [f"\n## Autores mais produtivos (top {a.top}) — nomes como vieram da base, sem desambiguação", "| Autor | Documentos |", "|---|---|"] + [f"| {k} | {v} |" for k, v in autores.most_common(a.top)]
    if a.citacoes:
        cit = {c["doi"].lower(): c.get("citacoes", 0) for c in json.load(open(a.citacoes)) if "erro" not in c}
        lista = sorted(((cit.get(col(r, "doi").lower().strip(), 0), col(r, "title")[:70], col(r, "year")) for r in rows if col(r, "doi").strip().lower() in cit), reverse=True)
        h = sum(1 for i, (c, _, _) in enumerate(lista, start=1) if c >= i)
        md += [f"\n## Citações (Crossref, {len(cit)} DOIs resolvidos) — índice h do corpus: **{h}**; total {sum(cit.values())}; sem citação: {sum(1 for v in cit.values() if v == 0)}", "| Citações | Título | Ano |", "|---|---|---|"] + [f"| {c} | {t} | {y} |" for c, t, y in lista[:a.top]]
    if a.figura:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        ys = sorted(anos); fig, ax = plt.subplots(figsize=(7, 3.6), dpi=150); ax.bar(ys, [anos[y] for y in ys]); ax.set_xlabel("Ano"); ax.set_ylabel("Documentos"); ax.set_title(f"Produção por ano (n = {len(rows)})"); fig.tight_layout(); fig.savefig(a.figura); md.append(f"\nfigura: {a.figura}")
    texto = "\n".join(md); print(texto)
    if a.markdown: open(a.markdown, "w", encoding="utf-8").write(texto + "\n"); print(f"\ngravado: {a.markdown}")

if __name__ == "__main__": main()
