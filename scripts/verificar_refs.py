#!/usr/bin/env python3
"""Resolve cada DOI citado num manuscrito na Crossref e imprime o metadado canônico.

    python3 verificar_refs.py manuscrito.md

✓ = existe; ✗ 404 = não existe (referência inventada); outro erro = verificar, não descartar.
Compare título, autores e ano com o que está na lista de referências (erro 2 do manual);
o erro 3 — artigo real que não diz aquilo — só cai na leitura da página.
"""
import re, sys, json, urllib.request

def crossref(doi):
    req = urllib.request.Request(f"https://api.crossref.org/works/{doi}",
                                 headers={"User-Agent": "verificar-refs (mailto:SEU@EMAIL)"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=20))["message"]
    except Exception as e:
        return {"erro": str(e)}

texto = open(sys.argv[1], encoding="utf-8").read()
for doi in sorted(set(re.findall(r"10\.\d{4,9}/[^\s\]\)\"'<>]+", texto))):
    m = crossref(doi.rstrip(".,;"))
    if "erro" in m:
        print("✗", doi, m["erro"]); continue
    autores = "; ".join(a.get("family", "") for a in m.get("author", []))
    ano = m.get("issued", {}).get("date-parts", [[None]])[0][0]
    print("✓", doi, "|", (m.get("title") or [""])[0][:70], "|", autores[:60], "|", ano)
