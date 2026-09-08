#!/usr/bin/env python3
"""Auditoria da biblioteca Zotero pela API local (Zotero 7+ aberto, com «Permitir que outros
aplicativos neste computador se comuniquem com o Zotero» ligado em Configurações → Avançado).

Aponta o que sai errado na lista de referências: itens sem DOI, sem PDF, capturados como
«Página da web», títulos em CAIXA ALTA, sem autor, sem ano, e prováveis duplicados.
Só lê; não altera nada. Uso:
    python3 auditar_biblioteca.py                     # biblioteca inteira
    python3 auditar_biblioteca.py --colecao "Revisao sistematica 2026"
    python3 auditar_biblioteca.py --csv auditoria.csv
"""
import argparse, csv, json, re, sys, urllib.parse, urllib.request
BASE="http://127.0.0.1:23119/api/users/0"
def get(path, **q):
    url=f"{BASE}{path}?{urllib.parse.urlencode(q)}"
    try:
        with urllib.request.urlopen(url, timeout=60) as r: return json.load(r)
    except Exception as e:
        sys.exit(f"Não consegui falar com o Zotero em {BASE} ({e}).\nAbra o Zotero e ligue a API local em Configurações → Avançado.")
def todos(path, **q):
    out=[]; start=0
    while True:
        lote=get(path, limit=100, start=start, **q)
        out+=lote
        if len(lote)<100: return out
        start+=100
ap=argparse.ArgumentParser(); ap.add_argument("--colecao"); ap.add_argument("--csv"); a=ap.parse_args()
path="/items/top"
if a.colecao:
    cols=[c for c in todos("/collections") if c["data"]["name"].lower()==a.colecao.lower()]
    if not cols: sys.exit(f"Coleção não encontrada: {a.colecao}")
    path=f"/collections/{cols[0]['key']}/items/top"
itens=todos(path)
filhos={}
for it in todos("/items"):
    p=it["data"].get("parentItem")
    if p: filhos.setdefault(p,[]).append(it["data"])
CITAVEIS={"journalArticle","book","bookSection","thesis","conferencePaper","report","preprint","standard","statute","document","manuscript","dataset","patent","magazineArticle","newspaperArticle"}
problemas=[]; vistos={}
for it in itens:
    d=it["data"]; tipo=d["itemType"]; titulo=(d.get("title") or "").strip(); k=it["key"]; probs=[]
    if tipo in ("attachment","note"): probs.append("anexo/nota sem item pai")
    if tipo=="webpage": probs.append("capturado como Página da web")
    if not titulo: probs.append("sem título")
    letras=[c for c in titulo if c.isalpha()]
    if len(letras)>12 and sum(c.isupper() for c in letras)/len(letras)>0.8: probs.append("título em CAIXA ALTA")
    if tipo in CITAVEIS and not d.get("creators"): probs.append("sem autor")
    if tipo in CITAVEIS and not re.search(r"\d{4}", d.get("date","") or ""): probs.append("sem ano")
    if tipo in ("journalArticle","conferencePaper","preprint","dataset") and not (d.get("DOI") or "").strip(): probs.append("sem DOI")
    doi=(d.get("DOI") or "").strip()
    if doi and not re.match(r"^10\.\S+/\S+$", doi): probs.append("DOI mal formado (deve ser só 10.xxxx/…)")
    tem_pdf=any(f.get("contentType")=="application/pdf" for f in filhos.get(k,[]))
    if tipo in CITAVEIS and not tem_pdf: probs.append("sem PDF anexado")
    chave=(doi.lower() if doi else re.sub(r"\W+","",titulo.lower()))
    if chave:
        if chave in vistos: probs.append(f"provável duplicado de {vistos[chave]}")
        else: vistos[chave]=k
    if probs: problemas.append((k,tipo,titulo[:70],"; ".join(probs)))
print(f"{len(itens)} itens auditados · {len(problemas)} com pendências\n")
for k,tipo,titulo,p in problemas: print(f"[{k}] {tipo:16s} {titulo}\n    → {p}")
if a.csv:
    with open(a.csv,"w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["chave","tipo","titulo","pendencias"]); w.writerows(problemas)
    print(f"\ncsv: {a.csv}")
