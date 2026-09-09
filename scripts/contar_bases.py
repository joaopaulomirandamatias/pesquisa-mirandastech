#!/usr/bin/env python3
"""A mesma pergunta em seis APIs abertas: mostra que cada base responde um total diferente.
    python3 contar_bases.py '"predictive maintenance" crane' --email seu@email.br
Só biblioteca padrão. Respeita os limites: 1 chamada por base; arXiv pede 3 s entre chamadas."""
import argparse, datetime, json, re, time, urllib.parse, urllib.request
def get(url, ua):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": ua}), timeout=60) as r: return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e: return e.code, ""
    except Exception as e: return -1, str(e)
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("consulta"); ap.add_argument("--email", required=True); a = ap.parse_args()
    q = urllib.parse.quote(a.consulta); ua = f"contar_bases.py (mailto:{a.email})"; hoje = datetime.date.today().isoformat(); linhas = []
    s, t = get(f"https://api.openalex.org/works?search={q}&per-page=1&mailto={a.email}", ua); linhas.append(("OpenAlex", "works?search=", json.loads(t)["meta"]["count"] if s == 200 else f"HTTP {s}"))
    s, t = get(f"https://api.crossref.org/works?query={q}&rows=0&mailto={a.email}", ua); linhas.append(("Crossref", "works?query= (relevância)", json.loads(t)["message"]["total-results"] if s == 200 else f"HTTP {s}"))
    termo = urllib.parse.quote(a.consulta.replace('"', '') and re.sub(r'\s+', ' AND ', re.sub(r'"([^"]+)"', r'"\1"[tiab]', a.consulta)))
    s, t = get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={termo}&retmax=0&retmode=json", ua); linhas.append(("PubMed", "esearch [tiab]", json.loads(t)["esearchresult"]["count"] if s == 200 else f"HTTP {s}"))
    s, t = get(f"https://export.arxiv.org/api/query?search_query=all:{q}&max_results=1", ua); m = re.search(r"totalResults[^>]*>(\d+)", t); linhas.append(("arXiv", "query?search_query=all:", m.group(1) if m else f"HTTP {s}")); time.sleep(3)
    s, t = get(f"https://doaj.org/api/search/articles/{q}?pageSize=1", ua); linhas.append(("DOAJ", "api/search/articles", json.loads(t)["total"] if s == 200 else f"HTTP {s}"))
    s, t = get(f"https://api.semanticscholar.org/graph/v1/paper/search?query={q}&limit=1", ua); linhas.append(("Semantic Scholar", "graph/v1/paper/search (sem chave)", json.loads(t).get("total") if s == 200 else f"HTTP {s}"))
    print(f"consulta: {a.consulta}   data: {hoje}"); print(f"{'base':<18}{'endpoint':<38}{'total':>10}")
    for b, e, n in linhas: print(f"{b:<18}{e:<38}{str(n):>10}")
    print("\n# totais diferentes são normais: cobertura, campos pesquisados e interpretação da consulta variam; registre todos no diário")
if __name__ == "__main__": main()
