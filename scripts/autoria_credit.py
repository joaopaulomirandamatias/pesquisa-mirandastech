#!/usr/bin/env python3
r"""Tabela de contribuições (CRediT) e checagem dos critérios de autoria (ICMJE) para um artigo ou capítulo, a preencher antes de escrever.

    python3 scripts/autoria_credit.py --titulo "…" --pessoas "Nome A;Nome B;Nome C" [--papeis "Nome A: Conceptualização, Investigação, Redação – rascunho original; Nome B: Supervisão, Redação – revisão e edição"] [--saida 06_texto/AUTORIA.md]

Gera a matriz pessoa × 14 papéis CRediT (marcando os informados), a lista dos 4 critérios do ICMJE para cada pessoa responder (sim/não) e a regra: só é autor quem cumpre os quatro; contribuição sem os quatro vai aos agradecimentos; ordem de autoria decidida agora e revista se mudar; chatbots não são autores e o uso de IA é declarado. Avisa quando alguém não tem papel algum ou tem só «Supervisão»/«Aquisição de financiamento» (ICMJE: não basta para autoria).
"""
import argparse, sys
from pathlib import Path

CREDIT = ["Conceptualização", "Curadoria de dados", "Análise formal", "Aquisição de financiamento", "Investigação", "Metodologia", "Administração de projeto", "Recursos", "Software", "Supervisão", "Validação", "Visualização", "Redação – rascunho original", "Redação – revisão e edição"]
ICMJE = ["Contribuição substancial à concepção ou ao desenho do trabalho, ou à aquisição, análise ou interpretação dos dados", "Redação do trabalho ou revisão crítica de conteúdo intelectual importante", "Aprovação final da versão a ser publicada", "Concordância em responder por todos os aspectos do trabalho (exatidão e integridade)"]

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--titulo", required=True); ap.add_argument("--pessoas", required=True); ap.add_argument("--papeis", default=""); ap.add_argument("--saida"); ap.add_argument("--forcar", action="store_true")
    a = ap.parse_args(); pessoas = [x.strip() for x in a.pessoas.split(";") if x.strip()]
    mapa = {p: set() for p in pessoas}
    for bloco in [b.strip() for b in a.papeis.split(";") if b.strip()]:
        nome, _, lista = bloco.partition(":"); nome = nome.strip()
        if nome not in mapa: sys.exit(f"pessoa desconhecida em --papeis: {nome}")
        for r in [x.strip() for x in lista.split(",") if x.strip()]:
            if r not in CREDIT: sys.exit(f"papel fora da taxonomia CRediT: {r}\n  válidos: {', '.join(CREDIT)}")
            mapa[nome].add(r)
    out = [f"# Autoria e contribuições — {a.titulo}", "", "## Papéis CRediT (marcar antes de escrever; rever se mudar)", "| Papel | " + " | ".join(pessoas) + " |", "|---|" + "---|" * len(pessoas)]
    for r in CREDIT: out.append(f"| {r} | " + " | ".join("✔" if r in mapa[p] else "" for p in pessoas) + " |")
    out += ["", "## Critérios de autoria (ICMJE) — cada pessoa responde sim/não aos quatro", "| Critério | " + " | ".join(pessoas) + " |", "|---|" + "---|" * len(pessoas)]
    for c in ICMJE: out.append(f"| {c} | " + " | ".join("[ ]" for _ in pessoas) + " |")
    out += ["", "## Regras", "- Autor é quem cumpre **os quatro** critérios; quem contribuiu sem os quatro vai aos agradecimentos (ex.: só financiamento, só supervisão geral, só revisão de linguagem).", "- Ordem de autoria: [decidir agora] — critério: [contribuição / alfabética / convenção da área]; revista se as contribuições mudarem.", "- Chatbots e assistentes de IA não são autores; o uso de IA é declarado (agradecimentos ou seção de métodos, conforme o periódico).", "- Ninguém entra por cortesia (autoria honorária) e ninguém que escreveu fica de fora (autoria fantasma).", ""]
    avisos = [f"AVISO {p}: nenhum papel CRediT informado" for p in pessoas if not mapa[p]] + [f"AVISO {p}: só «{', '.join(sorted(mapa[p]))}» — pelo ICMJE, supervisão geral ou financiamento não bastam para autoria" for p in pessoas if mapa[p] and mapa[p] <= {"Supervisão", "Aquisição de financiamento", "Recursos", "Administração de projeto"}]
    texto = "\n".join(out); print(texto); [print(v) for v in avisos]
    if a.saida:
        p = Path(a.saida)
        if p.exists() and not a.forcar: sys.exit(f"{p} já existe — use --forcar")
        p.parent.mkdir(parents=True, exist_ok=True); p.write_text(texto + "\n", encoding="utf-8"); print(f"\ngravado: {p}")

if __name__ == "__main__": main()
