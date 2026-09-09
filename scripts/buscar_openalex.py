#!/usr/bin/env python3
"""Busca reprodutível no OpenAlex (API gratuita, sem chave): percorre todas as páginas com cursor e grava
CSV (para o ASReview/planilha), RIS (para o Zotero) e um diário JSON com a consulta, os filtros, a data e o total.

    python3 buscar_openalex.py '"predictive maintenance" AND (port OR terminal OR crane)' \
        --campo title_and_abstract --desde 2015 --tipos article,book-chapter,preprint --email seu@email.br

--campo: title_and_abstract (padrão), title, abstract, fulltext, default (tudo) ou search (parâmetro search=, com stemming).
Só biblioteca padrão do Python 3.10+."""
import argparse, csv, datetime, json, sys, time, urllib.parse, urllib.request
API = "https://api.openalex.org/works"
CAMPOS = "id,doi,title,publication_year,authorships,primary_location,open_access,abstract_inverted_index,type"

def resumo(inv):
    if not inv: return ""
    pos = sorted((p, w) for w, ps in inv.items() for p in ps)
    return " ".join(w for _, w in pos)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("consulta"); ap.add_argument("--campo", default="title_and_abstract")
    ap.add_argument("--desde", type=int); ap.add_argument("--ate", type=int, default=datetime.date.today().year)
    ap.add_argument("--tipos", default=""); ap.add_argument("--email", required=True); ap.add_argument("--saida", default="busca_openalex")
    ap.add_argument("--max", type=int, default=10000, help="teto de registros (segurança)"); a = ap.parse_args()
    filtros = []
    if a.campo == "search": params = {"search": a.consulta}
    else: params = {}; filtros.append(f"{a.campo}.search:{a.consulta}")
    if a.desde: filtros.append(f"publication_year:{a.desde}-{a.ate}")
    if a.tipos: filtros.append("type:" + "|".join(a.tipos.split(",")))
    if filtros: params["filter"] = ",".join(filtros)
    params.update({"select": CAMPOS, "per-page": 200, "mailto": a.email, "cursor": "*"})
    registros, total, pagina = [], None, 0
    while True:
        url = API + "?" + urllib.parse.urlencode(params, safe='":()|,')
        if pagina == 0: print("GET", url.replace(a.email, "…"))
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": f"buscar_openalex.py (mailto:{a.email})"}), timeout=60) as r:
            d = json.load(r)
        total = d["meta"]["count"]; pagina += 1; registros += d["results"]
        print(f"meta.count = {total} · página {pagina} ({len(d['results'])} registros)")
        params["cursor"] = d["meta"].get("next_cursor")
        if not params["cursor"] or not d["results"] or len(registros) >= a.max: break
        time.sleep(0.2)
    linhas = []
    for w in registros:
        loc = w.get("primary_location") or {}; src = (loc.get("source") or {}).get("display_name", "")
        linhas.append({"title": w.get("title") or "", "abstract": resumo(w.get("abstract_inverted_index")), "year": w.get("publication_year"),
                       "doi": (w.get("doi") or "").replace("https://doi.org/", ""), "authors": "; ".join((au.get("author") or {}).get("display_name", "") for au in w.get("authorships", [])),
                       "source": src, "is_oa": (w.get("open_access") or {}).get("is_oa"), "type": w.get("type"), "openalex_id": w.get("id", "")})
    with open(a.saida + ".csv", "w", encoding="utf-8", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(linhas[0].keys()) if linhas else ["title"]); wr.writeheader(); wr.writerows(linhas)
    with open(a.saida + ".ris", "w", encoding="utf-8") as f:
        for l in linhas:
            f.write("TY  - JOUR\n" if l["type"] == "article" else "TY  - GEN\n"); f.write(f"TI  - {l['title']}\n")
            for au in l["authors"].split("; "):
                if au: f.write(f"AU  - {au}\n")
            if l["year"]: f.write(f"PY  - {l['year']}\n")
            if l["source"]: f.write(f"JO  - {l['source']}\n")
            if l["doi"]: f.write(f"DO  - {l['doi']}\n")
            if l["abstract"]: f.write(f"AB  - {l['abstract']}\n")
            f.write(f"UR  - {l['openalex_id']}\nER  - \n\n")
    hoje = datetime.date.today().isoformat()
    diario = {"base": "OpenAlex (api.openalex.org)", "data": hoje, "consulta": a.consulta, "campo": a.campo, "filtros": filtros, "total": total,
              "gravados": len(linhas), "com_resumo": sum(1 for l in linhas if l["abstract"]), "com_doi": sum(1 for l in linhas if l["doi"]), "script": "buscar_openalex.py"}
    json.dump(diario, open(f"diario_busca_{hoje}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"gravado: {a.saida}.csv ({len(linhas)} registros, {diario['com_resumo']} com resumo, {diario['com_doi']} com DOI)")
    print(f"gravado: {a.saida}.ris (para o Zotero: Arquivo → Importar…)"); print(f"gravado: diario_busca_{hoje}.json (cole no diário de busca / PRISMA-S)")

if __name__ == "__main__": main()
