#!/usr/bin/env python3
"""Relatório determinístico para o orientador, gerado só dos arquivos do projeto (nada é inventado):
fases e portas, checklists por papel com evidência, decisões datadas, uso de IA por etapa, pendências.
    python3 scripts/relatorio_orientador.py                       # imprime Markdown
    python3 scripts/relatorio_orientador.py --salvar               # grava 00_projeto/RELATORIO_ORIENTADOR.md
    python3 scripts/relatorio_orientador.py --html relatorio.html  # também em HTML simples"""
import csv, html, re, sys, datetime as dt
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from resumo_sessao import ler, tabela

def gerar(pasta="."):
    pasta = Path(pasta); r = ler(pasta)
    if r is None: raise SystemExit("PROGRESSO.md não encontrado nesta pasta.")
    txt = (pasta / "PROGRESSO.md").read_text(encoding="utf-8")
    hoje = dt.date.today().isoformat(); L = []
    L += [f"# Relatório para o orientador — {r['tema']}", "", f"Gerado em {hoje} a partir de `PROGRESSO.md`, `DECISOES.md` e `USO_DE_IA.csv`. Nenhuma linha abaixo foi escrita pelo agente: tudo vem dos arquivos.", ""]
    cab = re.search(r"^\*\*Método provável:\*\*.*$", txt, re.M)
    if cab: L += [cab.group(0), ""]
    fa = r["fase_atual"]
    L += ["## Onde o projeto está", "", f"- **Fase atual:** {fa['n']} — {fa['nome']}. Porta de saída: {fa['porta']}" if fa else "- **Todas as fases fechadas.**",
          f"- **Fases fechadas:** {', '.join(r['fases_fechadas']) or 'nenhuma'}",
          f"- **Última alteração do PROGRESSO.md:** há {r['dias_sem_alteracao']} dia(s)", ""]
    L += ["## Fases", "", "| Fase | Nome | Estado | Data | Evidência |", "|---|---|---|---|---|"]
    for f in tabela(txt, "| Fase | Nome |"):
        if len(f) >= 7: L.append(f"| {f[0]} | {f[1]} | {'fechada' if f[4].lower()=='[x]' else 'aberta'} | {f[5] or '—'} | {f[6] or '—'} |")
    nomes = {"M": "Método (Metodólogo)", "I": "Uso de IA (Orientador)", "B": "Biblioteca (Bibliotecário)", "L": "Leitura e síntese"}
    L += ["", "## Checklists: o que está feito e com que evidência", ""]
    for pref in "MIBL":
        linhas = re.findall(rf"^\| *({pref}\d+) *\| *([^|]*?) *\| *([^|]*?) *\| *[^|]*?\| *(\[[ xX]\]) *\| *([^|]*?) *\| *([^|]*?) *\|", txt, re.M)
        if not linhas: continue
        feitos = [l for l in linhas if l[3].lower() == "[x]"]
        L += [f"### {nomes[pref]} — {len(feitos)}/{len(linhas)}", ""]
        if feitos:
            L += ["| Item | Área | Data | Evidência conferida |", "|---|---|---|---|"]
            L += [f"| {a} | {b.strip()} | {e.strip() or '—'} | {ev.strip() or '(sem evidência anotada)'} |" for a, b, c, d, e, ev in feitos]
            L.append("")
        pend = [f"{a} ({b.strip()})" for a, b, c, d, e, ev in linhas if d.lower() != "[x]"]
        L += ["Pendentes: " + (", ".join(pend) if pend else "nenhum"), ""]
    L += ["## Decisões registradas (DECISOES.md)", ""]
    d = pasta / "DECISOES.md"
    if d.is_file():
        blocos = re.findall(r"^## (D\d+) — (.+?)\n((?:(?!^## ).*\n?)*)", d.read_text(encoding="utf-8"), re.M)
        reais = [(k, t, corpo) for k, t, corpo in blocos if re.search(r"\*\*Data:\*\* *\d{4}-\d{2}-\d{2}", corpo)]
        if reais:
            for k, t, corpo in reais:
                data = re.search(r"\*\*Data:\*\* *(\d{4}-\d{2}-\d{2})", corpo).group(1)
                resp = re.search(r"\*\*Respons[aá]vel:\*\* *([^·\n]+)", corpo); L.append(f"- **{k} — {t}** ({data}{', ' + resp.group(1).strip() if resp else ''})")
        else: L.append("Nenhuma decisão com data preenchida ainda (os esqueletos D001 e D002 não contam).")
    else: L.append("Arquivo ausente.")
    L += ["", "## Uso de IA declarado (USO_DE_IA.csv)", ""]
    u = pasta / "USO_DE_IA.csv"; linhas = []
    if u.is_file():
        with open(u, encoding="utf-8", newline="") as f: linhas = [x for x in csv.DictReader(f) if any((v or "").strip() for v in x.values())]
    if linhas:
        por = {}
        for x in linhas: por.setdefault(x.get("etapa", "?"), []).append(x)
        L += ["| Etapa | Registros | Ferramentas | Declara? |", "|---|---|---|---|"]
        for et, xs in por.items():
            L.append(f"| {et} | {len(xs)} | {', '.join(sorted({x.get('ferramenta','') for x in xs}))} | {', '.join(sorted({x.get('declara','') for x in xs}))} |")
        sem = [x for x in linhas if not (x.get("validacao") or "").strip()]
        L += ["", f"Registros sem validação anotada: {len(sem)}" if sem else "Todos os registros têm validação anotada."]
    else: L.append("Nenhum uso de IA registrado até agora.")
    L += ["", "## Para a reunião", "", "- Pergunte pela evidência de cada item marcado; um `[x]` sem arquivo, script ou número ao lado não conta.",
          "- Decisões sem data em `DECISOES.md` ainda não foram tomadas.", "- O próximo passo é sempre fechar a porta da fase atual antes de abrir material da seguinte.", ""]
    return "\n".join(L)

if __name__ == "__main__":
    md = gerar(".")
    if "--salvar" in sys.argv:
        out = Path("00_projeto/RELATORIO_ORIENTADOR.md") if Path("00_projeto").is_dir() else Path("RELATORIO_ORIENTADOR.md")
        out.write_text(md, encoding="utf-8"); print("gravado:", out)
    if "--html" in sys.argv:
        h = sys.argv[sys.argv.index("--html") + 1]; body = html.escape(md)
        Path(h).write_text(f"<!doctype html><meta charset='utf-8'><title>Relatório para o orientador</title><pre style='font:14px/1.5 sans-serif;white-space:pre-wrap;max-width:80ch;margin:2em auto'>{body}</pre>", encoding="utf-8"); print("gravado:", h)
    if "--salvar" not in sys.argv and "--html" not in sys.argv: print(md)
