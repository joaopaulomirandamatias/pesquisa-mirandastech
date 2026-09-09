#!/usr/bin/env python3
r"""Constrói redes bibliométricas a partir de um CSV e grava nos formatos do VOSviewer (map + network) e do VOSviewer Online (JSON).

    python3 scripts/mapa_vosviewer.py corpus.csv --tipo coautoria   --min 2 --saida coautoria
    python3 scripts/mapa_vosviewer.py corpus.csv --tipo termos      --min 5 --saida termos      (coocorrência de termos em título+resumo)
    python3 scripts/mapa_vosviewer.py corpus.csv --tipo fontes      --min 2 --saida fontes      (fontes ligadas por autores em comum)
    python3 scripts/mapa_vosviewer.py corpus.csv --tipo acoplamento --refs crossref_refs.json --min 1 --saida acoplamento

Contagem completa (full counting) como o padrão do VOSviewer: cada par que coocorre num documento soma 1 à força do link.
Saída: <saida>_map.txt (id, label, weight<Documents>, weight<Links>, weight<Total link strength>, score<Avg. pub. year>) e
<saida>_network.txt (id1, id2, força) para abrir no VOSviewer (File → Open) e <saida>.json para o VOSviewer Online
(app.vosviewer.com/?json=URL). Os agrupamentos (clusters) e as coordenadas são calculados pelo próprio VOSviewer ao abrir.
Termos: n-gramas de 1 a 3 palavras de título e resumo, em inglês, sem stopwords; sem lematização — use o thesaurus do VOSviewer para unir variantes.
"""
import argparse, csv, itertools, json, re
from collections import Counter, defaultdict

STOP = set("a an the of and or in on for to with by from at as is are was were be been this that these those we our it its into using use used based via than which who whose can may also not no such between among over under two three new one study studies paper approach approaches method methods results result proposed propose model models data analysis system systems performance high low different several various however therefore thus due within each both through their there here where when while during according respectively has have had having how including include includes presents present presented provides provide provided key role findings finding future current review across significant significantly improve improved improving developed develop developing has show shows shown showed potential important existing propose proposes address addresses addressing enable enables enabling allows allow allowing achieve achieved achieves reduce reduced reducing increase increased increasing overall main first second final total large small more most less least well highly widely often further also then only".split())

def col(r, *nomes):
    for n in nomes:
        for k in r:
            if k.lower().strip() == n: return r[k]
    return ""

def termos_doc(txt, nmax=3):
    toks = [t for t in re.findall(r"[a-z][a-z\-]+", txt.lower()) if t not in STOP and len(t) > 2]
    s = set()
    for n in range(1, nmax + 1):
        for i in range(len(toks) - n + 1):
            g = toks[i:i + n]
            if n > 1 and (g[0] in STOP or g[-1] in STOP): continue
            s.add(" ".join(g))
    return s

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("corpus"); ap.add_argument("--tipo", choices=["coautoria", "termos", "fontes", "acoplamento"], required=True)
    ap.add_argument("--min", type=int, default=2, help="mínimo de documentos (itens) para entrar no mapa"); ap.add_argument("--refs"); ap.add_argument("--saida", required=True); ap.add_argument("--max-itens", type=int, default=100)
    a = ap.parse_args(); rows = list(csv.DictReader(open(a.corpus, encoding="utf-8")))
    docs = []  # lista de (conjunto de itens, ano)
    if a.tipo == "acoplamento":
        refs = {c["doi"].lower(): set(c.get("refs_doi", [])) for c in json.load(open(a.refs)) if "erro" not in c}
        itens = {}; anos = {}
        for r in rows:
            d = col(r, "doi").lower().strip()
            if d in refs and refs[d]: itens[d] = refs[d]; anos[d] = col(r, "year")
        ids = sorted(itens); labels = {d: (col(next(r for r in rows if col(r, "doi").lower().strip() == d), "title")[:60]) for d in ids}
        links = Counter()
        for x, y in itertools.combinations(ids, 2):
            k = len(itens[x] & itens[y])
            if k: links[(x, y)] = k
        pesos = {d: 1 for d in ids}; ano_medio = {d: float(re.search(r"\d{4}", anos[d] or "0").group()) if re.search(r"\d{4}", anos[d] or "") else 0 for d in ids}
    else:
        pesos = Counter(); soma_ano = defaultdict(float)
        for r in rows:
            y = re.search(r"\d{4}", col(r, "year") or ""); y = int(y.group()) if y else None
            if a.tipo == "coautoria": s = {x.strip() for x in re.split(r";|\|", col(r, "authors", "author")) if x.strip()}
            elif a.tipo == "termos": s = termos_doc(col(r, "title") + ". " + col(r, "abstract"))
            else: s = {x.strip() for x in re.split(r";|\|", col(r, "authors", "author")) if x.strip()}
            if a.tipo == "fontes":
                docs.append((s, y, col(r, "source").strip())); continue
            docs.append((s, y))
            for x in s: pesos[x] += 1; soma_ano[x] += (y or 0)
        if a.tipo == "fontes":
            por_autor = defaultdict(set); pesos = Counter(); soma_ano = defaultdict(float)
            for s, y, f in docs:
                if not f: continue
                pesos[f] += 1; soma_ano[f] += (y or 0)
                for x in s: por_autor[x].add(f)
            links = Counter()
            for fs in por_autor.values():
                for p in itertools.combinations(sorted(fs), 2): links[p] += 1
        else:
            links = Counter()
            for s, y in docs:
                sel = [x for x in s if pesos[x] >= a.min]
                for p in itertools.combinations(sorted(sel), 2): links[p] += 1
        cand = [k for k, v in pesos.most_common() if v >= a.min]
        if a.tipo == "termos":  # descarta o termo curto quando um termo mais longo que o contém tem quase a mesma frequência (evita «maintenance» + «predictive maintenance»)
            longos = [k for k in cand if " " in k]
            cand = [k for k in cand if not any(k != l and k in l.split() and pesos[l] >= 0.8 * pesos[k] for l in longos)]
        ids = cand[:a.max_itens]; labels = {k: k for k in ids}; ano_medio = {k: soma_ano[k] / pesos[k] for k in ids}
    idset = set(ids); links = {p: v for p, v in links.items() if p[0] in idset and p[1] in idset}
    n_links = Counter(); forca = Counter()
    for (x, y), v in links.items(): n_links[x] += 1; n_links[y] += 1; forca[x] += v; forca[y] += v
    num = {k: i + 1 for i, k in enumerate(ids)}
    with open(f"{a.saida}_map.txt", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t"); w.writerow(["id", "label", "weight<Documents>", "weight<Links>", "weight<Total link strength>", "score<Avg. pub. year>"])
        for k in ids: w.writerow([num[k], labels[k], pesos[k], n_links[k], forca[k], f"{ano_medio[k]:.2f}"])
    with open(f"{a.saida}_network.txt", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        for (x, y), v in sorted(links.items(), key=lambda kv: -kv[1]): w.writerow([num[x], num[y], v])
    js = {"network": {"items": [{"id": num[k], "label": labels[k], "weights": {"Documents": pesos[k], "Links": n_links[k], "Total link strength": forca[k]}, "scores": {"Avg. pub. year": round(ano_medio[k], 2)}} for k in ids],
                      "links": [{"source_id": num[x], "target_id": num[y], "strength": v} for (x, y), v in links.items()]}}
    json.dump(js, open(f"{a.saida}.json", "w", encoding="utf-8"), ensure_ascii=False)
    isolados = sum(1 for k in ids if n_links[k] == 0)
    print(f"{a.tipo}: {len(rows)} documentos → {len(ids)} itens (mínimo {a.min}), {len(links)} links, {isolados} isolados; força total {sum(links.values())}\ngravados: {a.saida}_map.txt, {a.saida}_network.txt, {a.saida}.json")
    print("top 10 por documentos: " + "; ".join(f"{labels[k]} ({pesos[k]})" for k in ids[:10]))

if __name__ == "__main__": main()
