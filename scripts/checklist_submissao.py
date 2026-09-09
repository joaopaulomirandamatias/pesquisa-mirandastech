#!/usr/bin/env python3
"""Checklist de submissão de um artigo a um periódico, com o arquivo que prova cada item.

Uso:
  python3 checklist_submissao.py --periodico "Nome do periódico" [--issn 0000-0000] [--qualis A2]
        [--sistema "OJS|ScholarOne|Editorial Manager|…"] [--taxa "sem taxa|APC US$ …"] [--saida CHECKLIST_SUBMISSAO.md]

O checklist tem quatro momentos: escolher o periódico (perguntas do Think. Check. Submit.),
preparar os arquivos, submeter no sistema e acompanhar depois. Cada item pede a evidência
(o arquivo ou a tela) — o autor marca; o script não decide nada por ele.
"""
import argparse, datetime, sys
from pathlib import Path

ESCOLHER = [
    ("Você ou colegas conhecem o periódico e já leram artigos dele?", "lista de 3 artigos lidos (DOI)"),
    ("O nome do periódico é único e o ISSN confere no portal do ISSN?", "captura do portal.issn.org"),
    ("A editora aparece com nome, endereço e contato no site?", "URL da página «Sobre»"),
    ("O site diz como é a revisão por pares (quem revisa, quantos, tempo)?", "URL da política editorial"),
    ("O periódico está indexado onde a sua área busca (SciELO, Scopus, WoS, DOAJ…)?", "captura da indexação"),
    ("As taxas (APC) estão claras: valor, moeda, quando cobra, isenções?", "URL da página de taxas"),
    ("A licença de publicação e o que você pode depositar em repositório estão claros?", "URL da política de acesso aberto / Open policy finder"),
    ("A editora é membro do COPE (ética) e, se for acesso aberto, está no DOAJ?", "captura da lista de membros"),
    ("Qual é a classificação Qualis (quadriênio 2017-2020) do periódico na sua área?", "captura da Plataforma Sucupira"),
]
PREPARAR = [
    ("Manuscrito no formato exigido (estrutura, limite de palavras, idioma, referências)", "manuscrito.pdf / .docx"),
    ("Versão anonimizada quando a revisão é duplo-cega (sem nomes, afiliações, agradecimentos)", "manuscrito_anonimo.pdf"),
    ("Folha de rosto: título, autores na ordem acordada, afiliações, ORCID de todos, autor correspondente", "folha_de_rosto.pdf"),
    ("Carta de apresentação (cover letter) com escopo, contribuição e declarações", "CARTA_APRESENTACAO.md"),
    ("Contribuições por autor (CRediT) e concordância de todos com a versão enviada", "CREDIT.md + e-mails de aprovação"),
    ("Declaração de conflito de interesses e de financiamento", "conflito_interesses.pdf"),
    ("Aprovação ética (CEP/CAAE) quando a pesquisa envolve pessoas", "parecer_cep.pdf"),
    ("Disponibilidade de dados e código (repositório com DOI) ou justificativa", "DOI do depósito (Zenodo/OSF)"),
    ("Declaração de uso de IA, conforme a política do periódico", "USO_DE_IA.csv + declaração"),
    ("Figuras e tabelas em resolução e formato pedidos, com legendas e fontes", "pasta figuras/"),
    ("Preprint: a política do periódico permite? Se depositou, informe o DOI do preprint", "DOI do preprint ou «não depositado»"),
    ("Verificação de similaridade feita por você antes (citações com aspas e fonte)", "relatório de similaridade"),
]
SUBMETER = [
    ("Conta no sistema do periódico criada com o ORCID vinculado", "captura do perfil no sistema"),
    ("Metadados digitados iguais ao manuscrito (título, resumo, palavras-chave, autores, ORCID)", "captura da tela de metadados"),
    ("Arquivos enviados na ordem e com os nomes pedidos", "captura da lista de arquivos"),
    ("Revisores sugeridos/excluídos, se o sistema pedir (sem coautores nem pessoas do mesmo grupo)", "lista de sugeridos"),
    ("Confirmação de submissão recebida (número do manuscrito)", "e-mail de confirmação"),
]
DEPOIS = [
    ("Registrar a data e o status a cada mudança (com editor, em revisão, decisão)", "SUBMISSAO.md"),
    ("Decisão: responder ponto a ponto a cada revisor, no prazo (resposta_revisores.py)", "RESPOSTA_REVISORES.md"),
    ("Aceite: conferir provas, licença assinada, DOI atribuído", "provas.pdf + DOI"),
    ("Publicado: adicionar ao ORCID (por DOI) e ao Lattes; depositar a versão permitida no repositório", "captura do ORCID e do Lattes"),
    ("Rejeição: registrar o motivo, ajustar e escolher o próximo periódico — nunca submeter a dois ao mesmo tempo", "SUBMISSAO.md"),
]

def bloco(titulo, itens, inicio):
    out = [f"## {titulo}", "", "| # | Item | Evidência (arquivo ou tela) | Feito |", "|---|---|---|---|"]
    for i, (item, ev) in enumerate(itens, inicio):
        out.append(f"| {i} | {item} | {ev} | [ ] |")
    return out + [""], inicio + len(itens)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--periodico", required=True); ap.add_argument("--issn", default="—"); ap.add_argument("--qualis", default="consultar na Sucupira")
    ap.add_argument("--sistema", default="ver «Instruções aos autores»"); ap.add_argument("--taxa", default="ver página de taxas")
    ap.add_argument("--saida", default="CHECKLIST_SUBMISSAO.md")
    a = ap.parse_args()
    hoje = datetime.date.today().strftime("%d/%m/%Y")
    out = [f"# Checklist de submissão — {a.periodico}", "",
           f"- ISSN: {a.issn} · Qualis (2017-2020): {a.qualis} · Sistema de submissão: {a.sistema} · Taxas: {a.taxa}",
           f"- Gerado em {hoje} por checklist_submissao.py. Cada item pede a evidência; marque só com o arquivo em mãos.",
           "- Regra: um manuscrito, um periódico por vez. Quem decide submeter é o conjunto de autores.", ""]
    n = 1
    for t, it in (("1. Escolher o periódico (Think. Check. Submit.)", ESCOLHER), ("2. Preparar os arquivos", PREPARAR),
                  ("3. Submeter no sistema", SUBMETER), ("4. Depois da submissão", DEPOIS)):
        b, n = bloco(t, it, n); out += b
    total = n - 1
    Path(a.saida).write_text("\n".join(out), encoding="utf-8")
    print(f"gravado: {a.saida} ({total} itens em 4 momentos; periódico: {a.periodico})")
    print("próximo passo: preencher a coluna Evidência item a item; carta_apresentacao.py gera a carta.")

if __name__ == "__main__":
    main()
