#!/usr/bin/env python3
"""Compara os artigos do registro ORCID (API pública) com os do Currículo Lattes (XML exportado).

Uso:
  python3 orcid_lattes_diff.py --orcid 0000-0002-1825-0097 [--lattes curriculo.xml | curriculo.zip] [--saida DIFERENCAS.md]

- ORCID: lê pub.orcid.org/v3.0/<iD>/works (registro público; só o que está visível para «Everyone»).
- Lattes: lê o XML exportado do currículo (menu «Exportar» no Lattes; aceita o .zip com curriculo.xml)
  e extrai ARTIGO-PUBLICADO (título, ano, DOI, periódico).
- Compara por DOI (normalizado) e, sem DOI, por título; lista o que só está num lado.
O script não altera nenhum registro: ele mostra a lista para o autor decidir o que incluir onde.
"""
import argparse, json, re, sys, urllib.request, zipfile, io
import xml.etree.ElementTree as ET
from pathlib import Path

def norm_doi(d):
    d = (d or "").strip().lower(); d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d); return d or None
def norm_title(t): return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()

def orcid_works(iD):
    if not re.fullmatch(r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]", iD): sys.exit("iD ORCID inválido: use o formato 0000-0000-0000-0000")
    req = urllib.request.Request(f"https://pub.orcid.org/v3.0/{iD}/works", headers={"Accept": "application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=30)); w = []
    for g in d.get("group", []):
        s = g["work-summary"][0]; ids = {i["external-id-type"]: i["external-id-value"] for i in g["external-ids"]["external-id"]}
        ano = (s.get("publication-date") or {}).get("year") or {}
        w.append({"titulo": s["title"]["title"]["value"], "ano": ano.get("value", "—"), "doi": norm_doi(ids.get("doi")),
                  "tipo": s.get("type", ""), "fonte": (s["source"].get("source-name") or {}).get("value", "")})
    return w

def lattes_artigos(caminho):
    p = Path(caminho); raw = p.read_bytes()
    if p.suffix.lower() == ".zip":
        with zipfile.ZipFile(io.BytesIO(raw)) as z: raw = z.read([n for n in z.namelist() if n.lower().endswith(".xml")][0])
    root = ET.fromstring(raw); arts = []  # o parser respeita a declaração de codificação do XML (o Lattes exporta em ISO-8859-1)
    for a in root.iter("ARTIGO-PUBLICADO"):
        b = a.find("DADOS-BASICOS-DO-ARTIGO"); det = a.find("DETALHAMENTO-DO-ARTIGO")
        arts.append({"titulo": b.get("TITULO-DO-ARTIGO", ""), "ano": b.get("ANO-DO-ARTIGO", "—"), "doi": norm_doi(b.get("DOI")),
                     "periodico": det.get("TITULO-DO-PERIODICO-OU-REVISTA", "") if det is not None else ""})
    return arts

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--orcid", required=True); ap.add_argument("--lattes"); ap.add_argument("--saida", default="DIFERENCAS.md")
    a = ap.parse_args()
    o = orcid_works(a.orcid); print(f"ORCID {a.orcid}: {len(o)} trabalho(s) público(s)")
    for w in o: print(f"  {w['ano']}  {w['titulo'][:70]}  DOI {w['doi'] or '—'}  [{w['fonte']}]")
    if not a.lattes:
        print("sem --lattes: exporte o XML do currículo (Lattes → Exportar) para comparar."); return
    l = lattes_artigos(a.lattes); print(f"Lattes ({Path(a.lattes).name}): {len(l)} artigo(s) publicado(s)")
    key = lambda x: x["doi"] or "t:" + norm_title(x["titulo"])
    ko = {key(w): w for w in o}; kl = {key(x): x for x in l}
    so_orcid = [ko[k] for k in ko if k not in kl]; so_lattes = [kl[k] for k in kl if k not in ko]; ambos = [k for k in ko if k in kl]
    out = [f"# ORCID × Lattes — {a.orcid}", "", f"- ORCID: {len(o)} trabalho(s) · Lattes: {len(l)} artigo(s) · em ambos: {len(ambos)}", ""]
    for t, lst in (("Só no ORCID (candidatos a incluir no Lattes)", so_orcid), ("Só no Lattes (candidatos a incluir no ORCID, por DOI)", so_lattes)):
        out += [f"## {t} — {len(lst)}", "", "| Ano | Título | DOI |", "|---|---|---|"] + [f"| {x['ano']} | {x['titulo']} | {x['doi'] or '—'} |" for x in lst] + [""]
    out += ["Chave de comparação: DOI normalizado; sem DOI, o título. Nada foi alterado em nenhum registro — inclusão é decisão do autor."]
    Path(a.saida).write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"só no ORCID: {len(so_orcid)} · só no Lattes: {len(so_lattes)} · em ambos: {len(ambos)} → gravado: {a.saida}")

if __name__ == "__main__":
    main()
