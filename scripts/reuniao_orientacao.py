#!/usr/bin/env python3
r"""Registra uma reunião de orientação em REUNIOES.md: pauta, decisões, próximos passos com responsável e prazo; lista pendências abertas.

    python3 scripts/reuniao_orientacao.py --pauta "…;…" --decisoes "…;…" --proximos "quem: o quê até AAAA-MM-DD;…" [--presentes "…"] [--arquivo 00_projeto/REUNIOES.md]
    python3 scripts/reuniao_orientacao.py --pendencias            (lista os próximos passos ainda não marcados como feitos)

Cada reunião vira uma seção datada; os próximos passos são caixas «- [ ]» que o orientando marca ao concluir. Decisões relevantes também vão para o DECISOES.md (o script avisa). Nada é inventado: o script só grava o que foi passado.
"""
import argparse, datetime, re, sys
from pathlib import Path

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pauta", default=""); ap.add_argument("--decisoes", default=""); ap.add_argument("--proximos", default=""); ap.add_argument("--presentes", default="orientando; orientador")
    ap.add_argument("--arquivo", default="00_projeto/REUNIOES.md"); ap.add_argument("--pendencias", action="store_true"); ap.add_argument("--data", default=None)
    a = ap.parse_args(); p = Path(a.arquivo)
    if a.pendencias:
        if not p.exists(): sys.exit(f"{p} não existe")
        abertas = re.findall(r"^- \[ \] (.*)$", p.read_text(encoding="utf-8"), re.M); print(f"{len(abertas)} pendência(s) aberta(s) em {p}:"); [print(f"  - {x}") for x in abertas]; return
    if not (a.pauta or a.decisoes or a.proximos): sys.exit("informe --pauta, --decisoes e/ou --proximos (ou --pendencias)")
    data = a.data or datetime.date.today().isoformat(); sep = lambda s: [x.strip() for x in s.split(";") if x.strip()]
    bloco = [f"## Reunião de {data}", f"Presentes: {a.presentes}", ""]
    if a.pauta: bloco += ["**Pauta**"] + [f"- {x}" for x in sep(a.pauta)] + [""]
    if a.decisoes: bloco += ["**Decisões**"] + [f"- {x}" for x in sep(a.decisoes)] + [""]
    if a.proximos: bloco += ["**Próximos passos**"] + [f"- [ ] {x}" for x in sep(a.proximos)] + [""]
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists(): p.write_text("# Reuniões de orientação\n\n", encoding="utf-8")
    with p.open("a", encoding="utf-8") as f: f.write("\n".join(bloco) + "\n")
    n = len(re.findall(r"^## Reunião de", p.read_text(encoding="utf-8"), re.M))
    print(f"registrada: reunião de {data} em {p} ({n} reuniões no arquivo)")
    if a.decisoes: print("lembrete: decisões que mudam pergunta, método ou cronograma também vão para DECISOES.md com data e motivo")

if __name__ == "__main__": main()
