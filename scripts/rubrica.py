#!/usr/bin/env python3
r"""Gera a rubrica de uma entrega da disciplina (critérios × níveis) em Markdown, a partir dos modelos internos ou de critérios próprios.

    python3 scripts/rubrica.py --entrega projeto|busca|analise|texto|banca [--saida RUBRICA_projeto.md]
    python3 scripts/rubrica.py --entrega custom --criterios "Pergunta clara;Método justificado;Evidência anexada" --peso "40;40;20"

Níveis: 4 Atende com evidência · 3 Atende · 2 Parcial · 1 Não atende. Cada critério diz **qual arquivo prova** o nível (a rubrica avalia o artefato, não a intenção). Soma dos pesos = 100.
"""
import argparse, sys
from pathlib import Path

MODELOS = {
 "projeto": [("Pergunta delimitada, empírica e viável, com tabela vazia do resultado", 25, "PROGRESSO.md / PROJETO.md"), ("Método escolhido e justificado («escolhi X porque…; descartei Y porque…»)", 25, "PROJETO.md, DECISOES.md"), ("Ética e dados: CEP/TCLE quando há pessoas; plano de gestão de dados", 20, "03_etica/, PLANO_GESTAO_DADOS.md"), ("Cronograma e pré-registro (ou justificativa de não registrar)", 15, "CRONOGRAMA.md, PREREGISTRO.md"), ("Estrutura NBR 15287 e referências verificadas", 15, "PDF do projeto; verificar_refs.py")],
 "busca": [("String por conceitos, registrada verbatim com data e totais em ≥ 2 bases", 30, "BUSCA.md"), ("Biblioteca no Zotero auditada (DOI, autores, tipo) e .bib exportado", 25, "auditoria.csv, referencias.bib"), ("Deduplicação e triagem com codebook e decisão humana registrada", 25, "CONTAGENS.md, CODEBOOK.md"), ("Fluxograma PRISMA com números que fecham", 20, "fluxograma.png")],
 "analise": [("Limpeza documentada sem apagar linhas; decisões sobre ausentes/outliers", 20, "relatório do limpar_dados.py"), ("Técnica coerente com o projeto; pressupostos conferidos", 25, "DECISOES.md"), ("Resultado com n, efeito e IC (ou síntese qualitativa com trechos e codebook)", 30, "resultado.md / sintese.md"), ("Figura gerada por script, com unidade e n", 15, "*.png + script"), ("Relato conforme SAMPL/COREQ", 10, "seção de resultados")],
 "texto": [("Estrutura NBR 14724 e citações NBR 10520 sem erro de verificação", 25, "PDF; verificar_citacoes.py"), ("Referências NBR 6023 pelo gerenciador, DOIs resolvidos", 20, "verificar_refs.py"), ("Números do texto batem com as tabelas de origem", 20, "planilha/CSV de origem"), ("Repositório versionado com README/LICENSE/CITATION.cff, sem dado pessoal", 20, "checar_repo.py"), ("Declaração de uso de IA completa e verdadeira", 15, "USO_DE_IA.csv + declaração")],
 "banca": [("Roteiro com tempo por bloco e ensaio cronometrado", 30, "apresentacao.pdf, ensaio.csv"), ("Cinco objeções mais fortes com resposta honesta e correção no texto", 40, "banca.md"), ("Checklist do regimento preenchido", 30, "CHECKLIST_DEFESA.md")],
}
NIVEIS = ["4 · Atende com evidência anexada", "3 · Atende", "2 · Parcial", "1 · Não atende"]

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--entrega", required=True, choices=list(MODELOS) + ["custom"]); ap.add_argument("--criterios", default=""); ap.add_argument("--peso", default=""); ap.add_argument("--saida"); ap.add_argument("--forcar", action="store_true")
    a = ap.parse_args()
    if a.entrega == "custom":
        cs = [c.strip() for c in a.criterios.split(";") if c.strip()]; ps = [int(x) for x in a.peso.split(";")] if a.peso else [round(100 / len(cs))] * len(cs)
        if len(cs) != len(ps): sys.exit("critérios e pesos com tamanhos diferentes")
        itens = [(c, p, "[arquivo que prova]") for c, p in zip(cs, ps)]
    else: itens = MODELOS[a.entrega]
    if sum(p for _, p, _ in itens) != 100: sys.exit(f"pesos somam {sum(p for _, p, _ in itens)}, não 100")
    out = [f"# Rubrica — entrega «{a.entrega}»", "Nota = Σ peso × nível/4. A evidência é o arquivo, não o relato.", "", "| Critério | Peso | Evidência (arquivo) | " + " | ".join(NIVEIS) + " |", "|---|---|---|" + "---|" * 4]
    for c, p, ev in itens: out.append(f"| {c} | {p} | {ev} | " + " | ".join("[ ]" for _ in NIVEIS) + " |")
    out += ["", "Comentário ao estudante (o que muda na próxima versão): [preencher]"]
    texto = "\n".join(out); print(texto)
    if a.saida:
        p = Path(a.saida)
        if p.exists() and not a.forcar: sys.exit(f"{p} já existe — use --forcar")
        p.parent.mkdir(parents=True, exist_ok=True); p.write_text(texto + "\n", encoding="utf-8"); print(f"\ngravado: {p}")

if __name__ == "__main__": main()
