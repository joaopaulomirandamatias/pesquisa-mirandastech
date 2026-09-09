#!/usr/bin/env python3
"""Carta de apresentação (cover letter) para a submissão de um artigo.

Uso:
  python3 carta_apresentacao.py --titulo "…" --periodico "…" --contribuicao "…" --metodo "…" --resultado "…"
        [--autores "A; B; C"] [--correspondente "Nome <e-mail>"] [--lingua pt|en] [--financiamento "…"]
        [--etica "CAAE …"] [--dados "DOI …"] [--saida CARTA_APRESENTACAO.md]

A carta traz o que os editores costumam pedir: aderência ao escopo, contribuição, método e resultado
principal, e as declarações (originalidade, exclusividade, aprovação dos autores, conflito de
interesses, financiamento, ética, dados). Os campos vêm dos argumentos; nada é inventado —
o que faltar fica marcado como [PREENCHER].
"""
import argparse, datetime
from pathlib import Path

PT = {"sauda": "Prezada Editora, prezado Editor,", "abre": "Submetemos à apreciação de {p} o manuscrito «{t}», para publicação como {tipo}.",
      "escopo": "O trabalho adere ao escopo do periódico porque {c}",
      "metodo": "Método: {m}", "resultado": "Resultado principal: {r}",
      "decl": ["O manuscrito é original, não foi publicado e não está sob avaliação em outro periódico.",
               "Todos os autores leram e aprovaram a versão submetida e concordam com a ordem de autoria; as contribuições seguem a taxonomia CRediT (arquivo anexo).",
               "Conflito de interesses: {coi}", "Financiamento: {fin}", "Ética: {et}", "Dados e código: {dad}",
               "Uso de IA: {ia}"],
      "fecha": "Agradecemos a atenção e ficamos à disposição.", "corr": "Autor(a) correspondente: {corr}", "tipo": "artigo original",
      "coi": "os autores declaram não haver conflito de interesses.", "fin": "[PREENCHER — agência e número do processo, ou «sem financiamento»]",
      "et": "[PREENCHER — CAAE/parecer do CEP, ou «não se aplica: pesquisa sem seres humanos»]", "dad": "[PREENCHER — DOI do depósito ou justificativa]",
      "ia": "[PREENCHER — ferramentas, etapas e finalidade, conforme a política do periódico, ou «não houve uso»]"}
EN = {"sauda": "Dear Editor,", "abre": "We submit for consideration in {p} the manuscript “{t}”, as {tipo}.",
      "escopo": "The work fits the journal's scope because {c}",
      "metodo": "Method: {m}", "resultado": "Main result: {r}",
      "decl": ["The manuscript is original, has not been published and is not under consideration elsewhere.",
               "All authors have read and approved the submitted version and agree with the authorship order; contributions follow the CRediT taxonomy (attached).",
               "Competing interests: {coi}", "Funding: {fin}", "Ethics: {et}", "Data and code: {dad}", "Use of AI: {ia}"],
      "fecha": "Thank you for your consideration.", "corr": "Corresponding author: {corr}", "tipo": "an original article",
      "coi": "the authors declare no competing interests.", "fin": "[FILL IN — agency and grant number, or “no funding”]",
      "et": "[FILL IN — ethics approval number, or “not applicable”]", "dad": "[FILL IN — DOI of the deposit or justification]",
      "ia": "[FILL IN — tools, stages and purpose, per the journal policy, or “none”]"}

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for k in ("titulo", "periodico", "contribuicao", "metodo", "resultado"): ap.add_argument("--" + k, required=True)
    ap.add_argument("--autores", default="[PREENCHER]"); ap.add_argument("--correspondente", default="[PREENCHER]")
    ap.add_argument("--lingua", choices=["pt", "en"], default="pt"); ap.add_argument("--tipo", default=None)
    ap.add_argument("--financiamento"); ap.add_argument("--etica"); ap.add_argument("--dados"); ap.add_argument("--ia"); ap.add_argument("--coi")
    ap.add_argument("--saida", default="CARTA_APRESENTACAO.md")
    a = ap.parse_args(); L = PT if a.lingua == "pt" else EN
    hoje = datetime.date.today().strftime("%d/%m/%Y" if a.lingua == "pt" else "%Y-%m-%d")
    decl = [d.format(coi=a.coi or L["coi"], fin=a.financiamento or L["fin"], et=a.etica or L["et"], dad=a.dados or L["dad"], ia=a.ia or L["ia"]) for d in L["decl"]]
    out = [f"{hoje}", "", L["sauda"], "", L["abre"].format(p=a.periodico, t=a.titulo, tipo=a.tipo or L["tipo"]), "",
           L["escopo"].format(c=a.contribuicao), "", L["metodo"].format(m=a.metodo), "", L["resultado"].format(r=a.resultado), "",
           *[f"- {d}" for d in decl], "", L["fecha"], "", a.autores, L["corr"].format(corr=a.correspondente)]
    Path(a.saida).write_text("\n".join(out) + "\n", encoding="utf-8")
    faltam = sum(1 for d in decl if "PREENCHER" in d or "FILL IN" in d) + sum(1 for x in (a.autores, a.correspondente) if "PREENCHER" in x)
    print(f"gravado: {a.saida} ({a.lingua}; {len(decl)} declarações; {faltam} campo(s) marcado(s) para preencher)")
    print("\n".join(out))

if __name__ == "__main__":
    main()
