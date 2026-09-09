#!/usr/bin/env python3
"""Monta a resposta ponto a ponto aos revisores a partir do texto da decisão editorial.

Uso:
  python3 resposta_revisores.py comentarios.txt [--saida RESPOSTA_REVISORES.md]

O arquivo de entrada é o texto colado do e-mail/sistema: blocos «Revisor 1», «Reviewer 2», «Editor»…
e, dentro deles, comentários numerados («1.», «1)», «-», «•»). O script separa cada comentário
numa linha da tabela com as colunas Resposta e Alteração (página/linha) em branco — quem
responde é o autor. Sem marcar «aceito»/«recusado» sozinho: ele só organiza.
"""
import argparse, re, sys
from pathlib import Path

CAB = re.compile(r"^\s*(revisor|reviewer|referee|parecerista|editor)\s*[:#]?\s*([0-9]+|[A-Z])?\s*[:.\-—]?\s*$", re.I)
ITEM = re.compile(r"^\s*(?:(\d+)[.)]|[-•*])\s+(.*)$")

def parse(texto):
    blocos = []; atual = None
    for linha in texto.splitlines():
        if not linha.strip(): continue
        m = CAB.match(linha)
        if m:
            nome = m.group(1).capitalize() + (f" {m.group(2)}" if m.group(2) else ""); atual = {"nome": nome, "itens": []}; blocos.append(atual); continue
        if atual is None: atual = {"nome": "Editor", "itens": []}; blocos.append(atual)
        mi = ITEM.match(linha)
        if mi: atual["itens"].append(mi.group(2).strip())
        elif atual["itens"]: atual["itens"][-1] += " " + linha.strip()
        else: atual["itens"].append(linha.strip())
    return blocos

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada"); ap.add_argument("--saida", default="RESPOSTA_REVISORES.md")
    a = ap.parse_args()
    texto = Path(a.entrada).read_text(encoding="utf-8"); blocos = parse(texto)
    if not blocos: sys.exit("nenhum comentário reconhecido — cole o texto da decisão com os blocos «Revisor 1», «Revisor 2»…")
    out = ["# Resposta aos revisores", "", "Agradecemos aos revisores e ao editor pelos comentários. Respondemos a cada ponto abaixo; as alterações estão marcadas no manuscrito revisado.", ""]
    total = 0
    for b in blocos:
        out += [f"## {b['nome']} ({len(b['itens'])} comentário(s))", "", "| # | Comentário | Resposta | Alteração (página/linha) |", "|---|---|---|---|"]
        for i, c in enumerate(b["itens"], 1):
            out.append(f"| {b['nome'][0]}{i} | {c} | [PREENCHER] | [PREENCHER] |"); total += 1
        out.append("")
    out += ["## Regras que seguimos", "- Cada comentário recebe uma resposta, mesmo quando discordamos (com argumento e fonte).",
            "- Toda alteração aponta a página/linha da versão revisada; o que não mudou diz por quê.", "- Prazo da resposta anotado em SUBMISSAO.md."]
    Path(a.saida).write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"gravado: {a.saida} — {len(blocos)} bloco(s), {total} comentário(s) a responder")
    for b in blocos: print(f"  {b['nome']}: {len(b['itens'])}")

if __name__ == "__main__":
    main()
