#!/usr/bin/env python3
r"""Painel da turma: lê o PROGRESSO.md de cada pasta de estudante e mostra, sem juízo, a fase atual, as fases fechadas e há quantos dias cada projeto não muda.

    python3 scripts/turma_progresso.py <pasta_da_turma> [--markdown painel.md]

Espera uma pasta com uma subpasta por estudante (cada uma com PROGRESSO.md gerado por iniciar_projeto.py). Nada é inventado: quem não tem PROGRESSO.md aparece como «sem projeto». Serve para o professor ver quem precisa de conversa — não para nota.
"""
import argparse, re, sys, datetime as dt
from pathlib import Path

def ler(p):
    txt = p.read_text(encoding="utf-8"); linhas = re.findall(r"^\| *(\d+) *\| *([^|]+?) *\|[^|]*\|[^|]*\| *(\[[ xX]\]) *\|", txt, re.M)
    fechadas = [n for n, _, m in linhas if m.lower() == "[x]"]; atual = next(((n, nome) for n, nome, m in linhas if m.lower() != "[x]"), None)
    dias = (dt.date.today() - dt.date.fromtimestamp(p.stat().st_mtime)).days
    tema = re.search(r"^# Progresso — (.*)$", txt, re.M) or re.search(r"^\*\*Tema:\*\*\s*(.*)$", txt, re.M)
    return {"fechadas": fechadas, "atual": atual, "dias": dias, "tema": tema.group(1).strip() if tema else ""}

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pasta"); ap.add_argument("--markdown"); a = ap.parse_args()
    raiz = Path(a.pasta); alunos = sorted(d for d in raiz.iterdir() if d.is_dir() and not d.name.startswith("."))
    if not alunos: sys.exit("nenhuma subpasta encontrada")
    out = [f"# Painel da turma — {raiz.name} ({dt.date.today().isoformat()})", "", "| Estudante (pasta) | Tema | Fase atual | Fases fechadas | Dias sem alteração |", "|---|---|---|---|---|"]; alerta = []
    for d in alunos:
        p = d / "PROGRESSO.md"
        if not p.exists(): out.append(f"| {d.name} | — | sem projeto (rode iniciar_projeto.py) | — | — |"); alerta.append(d.name); continue
        r = ler(p); fa = f"{r['atual'][0]} — {r['atual'][1]}" if r["atual"] else "todas fechadas"
        out.append(f"| {d.name} | {r['tema'][:40]} | {fa} | {', '.join(r['fechadas']) or 'nenhuma'} | {r['dias']} |")
        if r["dias"] > 14: alerta.append(d.name)
    out += ["", f"Projetos parados há mais de 14 dias ou sem projeto: {', '.join(alerta) if alerta else 'nenhum'} — motivo para conversa, não para nota."]
    texto = "\n".join(out); print(texto)
    if a.markdown: Path(a.markdown).write_text(texto + "\n", encoding="utf-8"); print(f"\ngravado: {a.markdown}")

if __name__ == "__main__": main()
