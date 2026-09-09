#!/usr/bin/env python3
"""Resumo curto do projeto para o início da sessão (hook SessionStart) ou para o Pesquisador.
Lê PROGRESSO.md, DECISOES.md e USO_DE_IA.csv da pasta atual. Só lê; imprime até ~8 linhas.
    python3 resumo_sessao.py            # texto
    python3 resumo_sessao.py --json     # dicionário com os mesmos dados"""
import csv, json, os, re, sys, datetime as dt
from pathlib import Path

def tabela(txt, cabecalho):
    """Linhas de uma tabela Markdown cujo cabeçalho começa por `cabecalho`."""
    i = txt.find(cabecalho)
    if i < 0: return []
    linhas = []
    for l in txt[i:].splitlines()[2:]:
        if not l.startswith("|"): break
        linhas.append([c.strip() for c in l.strip("|").split("|")])
    return linhas

def ler(pasta="."):
    pasta = Path(pasta); p = pasta / "PROGRESSO.md"
    if not p.is_file(): return None
    txt = p.read_text(encoding="utf-8")
    tema = (re.search(r"^# Progresso — (.+)$", txt, re.M) or [None, ""])[1]
    esquema = int((re.search(r"<!-- esquema: (\d+)", txt) or [None, "0"])[1])
    fases = tabela(txt, "| Fase | Nome |")
    fechadas = [f for f in fases if len(f) > 4 and f[4].lower() == "[x]"]
    abertas = [f for f in fases if len(f) > 4 and f[4].lower() != "[x]"]
    atual = abertas[0] if abertas else None
    checks = {}
    itens = re.findall(r"^\| ([MIBL])(\d+) \|[^\n]*\| (\[[ xX]\]) \|", txt, re.M)
    for pref, n, est in itens:
        c = checks.setdefault(pref, {"feitos": 0, "total": 0}); c["total"] += 1
        if est.lower() == "[x]": c["feitos"] += 1
    mod = dt.datetime.fromtimestamp(p.stat().st_mtime); dias = (dt.datetime.now() - mod).days
    ultima = None
    d = pasta / "DECISOES.md"
    if d.is_file():
        blocos = re.findall(r"^## (D\d+) — (.+?)\n\*\*Data:\*\* *([^·\n]+)", d.read_text(encoding="utf-8"), re.M)
        reais = [(k, t.strip(), dta.strip()) for k, t, dta in blocos if re.match(r"\d{4}-\d{2}-\d{2}", dta.strip())]
        if reais: ultima = reais[-1]
    usos = 0; u = pasta / "USO_DE_IA.csv"
    if u.is_file():
        with open(u, encoding="utf-8", newline="") as f: usos = sum(1 for r in csv.DictReader(f) if any(r.values()))
    return {"tema": tema, "esquema": esquema, "fase_atual": atual and {"n": atual[0], "nome": atual[1], "porta": atual[2]},
            "fases_fechadas": [f[0] for f in fechadas], "checklists": checks, "dias_sem_alteracao": dias,
            "ultima_decisao": ultima and {"id": ultima[0], "titulo": ultima[1], "data": ultima[2]}, "usos_de_ia": usos}

def texto(r):
    if not r: return ""
    out = [f"Projeto de pesquisa MirandasTech: {r['tema']}"]
    fa = r["fase_atual"]
    out.append(f"Fase atual: {fa['n']} — {fa['nome']} (porta: {fa['porta']})" if fa else "Todas as onze fases fechadas.")
    out.append("Fases fechadas: " + (", ".join(r["fases_fechadas"]) or "nenhuma"))
    ck = " · ".join(f"{k} {v['feitos']}/{v['total']}" for k, v in sorted(r["checklists"].items()))
    if ck: out.append("Checklists: " + ck)
    ud = r["ultima_decisao"]
    out.append(f"Última decisão: {ud['id']} — {ud['titulo']} ({ud['data']})" if ud else "Nenhuma decisão datada em DECISOES.md ainda.")
    out.append(f"Usos de IA registrados: {r['usos_de_ia']} · PROGRESSO.md sem alteração há {r['dias_sem_alteracao']} dia(s)")
    out.append('Diga: "Pesquisador, onde paramos?"')
    return "\n".join(out)

if __name__ == "__main__":
    r = ler(".")
    if r is None: sys.exit(0)
    print(json.dumps(r, ensure_ascii=False, indent=1) if "--json" in sys.argv else texto(r))
