#!/usr/bin/env python3
r"""Gera o CITATION.cff (Citation File Format 1.2.0) do repositório e mostra como ele será citado.

    python3 scripts/citacao_cff.py --titulo "…" --autores "Sobrenome, Nome; Sobrenome, Nome" --versao 1.0 \
        --data 2026-09-09 [--doi 10.5281/zenodo.NNN] [--url https://github.com/…] [--licenca CC-BY-4.0] [--orcid 0000-…;0000-…] [--saida CITATION.cff]

O GitHub lê o arquivo na raiz e mostra o botão «Cite this repository» (APA e BibTeX); o Zenodo usa os mesmos
metadados ao arquivar uma release. O script escreve o arquivo (recusa sobrescrever sem --forcar) e imprime
a entrada BibTeX (@software) e a referência no padrão ABNT para conferência.
"""
import argparse, sys
from pathlib import Path

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--titulo", required=True); ap.add_argument("--autores", required=True, help='"Sobrenome, Nome; Sobrenome, Nome"')
    ap.add_argument("--versao", required=True); ap.add_argument("--data", required=True, help="AAAA-MM-DD")
    ap.add_argument("--doi", default=""); ap.add_argument("--url", default=""); ap.add_argument("--licenca", default="", help="identificador SPDX, ex.: MIT, CC-BY-4.0")
    ap.add_argument("--orcid", default="", help="lista na mesma ordem dos autores, separada por ;")
    ap.add_argument("--saida", default="CITATION.cff"); ap.add_argument("--forcar", action="store_true")
    a = ap.parse_args()
    autores = [x.strip() for x in a.autores.split(";") if x.strip()]
    orcids = [x.strip() for x in a.orcid.split(";")] if a.orcid else []
    if not all("," in x for x in autores): sys.exit('erro: cada autor como "Sobrenome, Nome"')
    if len(a.data) != 10: sys.exit("erro: --data no formato AAAA-MM-DD")
    linhas = ["cff-version: 1.2.0", "message: \"Se você usar este software ou material, cite-o como abaixo.\"", f"title: \"{a.titulo}\"",
              f"version: \"{a.versao}\"", f"date-released: {a.data}", "authors:"]
    for i, x in enumerate(autores):
        fam, dado = [s.strip() for s in x.split(",", 1)]
        linhas += [f"  - family-names: \"{fam}\"", f"    given-names: \"{dado}\""]
        if i < len(orcids) and orcids[i]: linhas.append(f"    orcid: \"https://orcid.org/{orcids[i]}\"")
    if a.doi: linhas.append(f"doi: {a.doi}")
    if a.url: linhas.append(f"url: \"{a.url}\"")
    if a.licenca: linhas.append(f"license: {a.licenca}")
    saida = Path(a.saida)
    if saida.exists() and not a.forcar: sys.exit(f"{saida} já existe — use --forcar para sobrescrever")
    saida.write_text("\n".join(linhas) + "\n", encoding="utf-8"); print(f"gravado: {saida}\n")
    print("\n".join(linhas)); print()
    chave = autores[0].split(",")[0].lower().replace(" ", "") + a.data[:4]
    nomes_bib = " and ".join(autores)
    print("BibTeX (@software, como o GitHub gera):")
    print(f"@software{{{chave},\n  author = {{{nomes_bib}}},\n  title = {{{a.titulo}}},\n  version = {{{a.versao}}},\n  year = {{{a.data[:4]}}},\n  month = {{{int(a.data[5:7])}}}," + (f"\n  doi = {{{a.doi}}}," if a.doi else "") + (f"\n  url = {{{a.url}}}," if a.url else "") + "\n}\n")
    abnt = "; ".join(f"{fam.upper()}, {''.join(p[0] + '. ' for p in dado.split())}".strip() for fam, dado in (map(str.strip, x.split(",", 1)) for x in autores))
    print("Referência (padrão ABNT para software, conferir com a biblioteca):")
    print(f"{abnt} {a.titulo}. Versão {a.versao}. [S. l.], {a.data[:4]}." + (f" DOI: {a.doi}." if a.doi else "") + (f" Disponível em: {a.url}." if a.url else "") + " Acesso em: (data).")

if __name__ == "__main__": main()
