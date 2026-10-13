#!/usr/bin/env python3
r"""Gera o plano de ensino de uma disciplina de metodologia/pesquisa em Markdown, com cronograma semana a semana ligado aos manuais MirandasTech e às entregas com evidência.

    python3 scripts/plano_de_ensino.py --disciplina "…" --semanas 17 [--carga 60] [--nivel graduacao|pos] [--saida PLANO_DE_ENSINO.md]

Estrutura: ementa, objetivos (o que o estudante entrega, não «conhecer»), cronograma (semana, tema, manual e slides, atividade em aula, entrega com evidência), avaliação (rubricas por entrega, sem prova de memorização), regras de uso de IA na disciplina (declarar, verificar, não substituir a leitura), bibliografia (manuais CC BY 4.0 + obras que o professor escolher). O cronograma padrão de 17 semanas segue as fases do Pesquisador (diagnóstico → entrega) e fecha com a submissão do artigo e o estágio de docência; com outro número de semanas, as fases são comprimidas ou expandidas proporcionalmente.
"""
import argparse, datetime, sys
from pathlib import Path

FASES = [("Diagnóstico e pasta do projeto", "Uso de IA na pesquisa · Plugin", "criar a pasta com iniciar_projeto.py; acordo de uso de IA", "PROGRESSO.md criado; USO_DE_IA.csv"),
         ("Tema → problema → pergunta", "Metodologia (slides 7–9)", "oficina: da ideia à pergunta com tabela vazia do resultado", "pergunta + objetivos no PROGRESSO.md"),
         ("Método e desenho", "Metodologia (12–16)", "classificar o estudo; escolher e justificar o método", "frase «escolhi X porque…; descartei Y porque…»"),
         ("Projeto e ética", "Metodologia (25–28) · Ciência aberta", "esqueleto NBR 15287; pré-registro; plano de gestão de dados", "PROJETO.md; PREREGISTRO.md; PGD"),
         ("Busca em bases", "Busca em bases", "montar a string com Bramer; rodar em duas bases; diário", "BUSCA.md com strings verbatim e totais"),
         ("Biblioteca no Zotero", "Zotero", "importar, organizar coleções, auditar metadados", "auditoria sem erro; .bib exportado"),
         ("Triagem e revisão sistemática", "Revisão sistemática com PRISMA", "deduplicar; triar no ASReview; kappa; fluxograma", "CONTAGENS.md; fluxograma PRISMA"),
         ("Leitura e síntese", "Gemini Notebook", "fichamento com página; matriz de síntese", "matriz de síntese conferida"),
         ("Bibliometria do campo", "Bibliometria", "indicadores e mapa de termos do corpus", "indicadores.md; mapa aberto no VOSviewer Online"),
         ("Dados: limpeza e análise", "Análise de dados", "limpar_dados.py; analisar.py; figura por script", "relatório de limpeza; resultado com efeito e IC"),
         ("Qualitativo com o Taguette", "Análise de dados (Parte 5)", "codebook; codificar; exportar; síntese", "codebook; sintese.md com trechos"),
         ("Escrita em LaTeX/ABNT", "LaTeX com Overleaf e abnTeX2", "novo_trabalho.py; citar do .bib; compilar", "PDF sem «??»; checar_citacoes.py sem erro"),
         ("Versão e publicação", "Git e GitHub · Ciência aberta", "commits por marco; README/LICENSE/CITATION.cff; depósito", "repositório auditado; .zenodo.json"),
         ("Pré-banca", "Defesa e qualificação", "roteiro; ensaio cronometrado; banca simulada", "banca.md; ensaio.csv"),
         ("Entrega e declaração de uso de IA", "Uso de IA (43) · Plugin", "checklist final; relatório do orientador", "RELATORIO_ORIENTADOR.md; declaração de IA"),
         ("Submissão do artigo", "Submissão de artigos, ORCID e Lattes", "escolher o periódico com o Think. Check. Submit.; checklist_submissao.py; carta de apresentação", "CHECKLIST_SUBMISSAO.md; CARTA_APRESENTACAO.md"),
         ("Estágio de docência", "Manual do professor", "conduzir uma semana do cronograma sob supervisão; rubrica da entrega com rubrica.py", "plano da semana conduzida; rubrica da entrega")]

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--disciplina", required=True); ap.add_argument("--semanas", type=int, default=17); ap.add_argument("--carga", type=int, default=60); ap.add_argument("--nivel", choices=["graduacao", "pos"], default="pos"); ap.add_argument("--saida"); ap.add_argument("--forcar", action="store_true")
    a = ap.parse_args(); hoje = datetime.date.today().isoformat()
    n = a.semanas; idx = [round(i * len(FASES) / n) for i in range(n)]; idx = [min(i, len(FASES) - 1) for i in idx]
    out = [f"# Plano de ensino — {a.disciplina}", f"Carga horária: {a.carga} h · {n} semanas · nível: {'pós-graduação' if a.nivel == 'pos' else 'graduação'} · rascunho gerado em {hoje} (modelo MirandasTech; ajuste ao PPC e ao regimento).", "",
           "## Ementa", "Da pergunta ao trabalho entregue: método, projeto e ética, busca e biblioteca, triagem e revisão, leitura e síntese, análise, escrita ABNT, versão e publicação, banca, submissão do artigo e estágio de docência — com uso declarado e verificado de IA.", "",
           "## Objetivos (o que o estudante entrega)", "- Um projeto de pesquisa próprio, em fases, com evidência de cada etapa no `PROGRESSO.md`.", "- Buscas reprodutíveis, biblioteca auditada, corpus triado e sintetizado.", "- Um resultado analisado com efeito e intervalo (ou síntese qualitativa com trechos), figura por script.", "- Texto no padrão ABNT, versionado, com declaração de uso de IA e material depositado.", "",
           "## Cronograma", "| Semana | Tema | Manual (slides) | Em aula | Entrega (evidência) |", "|---|---|---|---|---|"]
    for w, i in enumerate(idx, start=1):
        t, m, aula, ent = FASES[i]; out.append(f"| {w} | {t} | {m} | {aula} | {ent} |")
    out += ["", "## Avaliação", "- Por entregas com evidência (rubricas em `rubrica.py`): projeto (20 %), busca + biblioteca + triagem (20 %), análise ou síntese (20 %), texto final (25 %), pré-banca e declaração de IA (15 %). Sem prova de memorização.", "- Cada entrega é conferida pelo arquivo, não pelo relato: string verbatim, log de compilação, CSV de ensaio, auditoria do repositório.", "- Recuperação: nova versão da entrega com o que mudou e por quê (DECISOES.md).", "",
            "## Uso de IA na disciplina", "- Permitido com registro em `USO_DE_IA.csv` (ferramenta, fase, finalidade, validação) e declaração no texto; proibido gerar dados, resumir fontes não lidas ou assinar texto gerado como próprio (CNPq).", "- O plugin Pesquisa MirandasTech pode conduzir as fases; o estudante decide e o professor confere a evidência.", "",
            "## Bibliografia", "- Manuais MirandasTech (CC BY 4.0): https://www.mirandastech.com.br/pesquisa — citar cada um como `MATIAS, J. P. M. <título>. MirandasTech, v1.0, set. 2026.`", "- Obras da área escolhidas pelo professor: [preencher com referências verificadas].", ""]
    texto = "\n".join(out)
    if a.saida:
        p = Path(a.saida)
        if p.exists() and not a.forcar: sys.exit(f"{p} já existe — use --forcar")
        p.parent.mkdir(parents=True, exist_ok=True); p.write_text(texto, encoding="utf-8"); print(f"gravado: {p} ({n} semanas, {len(set(idx))} fases cobertas)")
    else: print(texto)

if __name__ == "__main__": main()
