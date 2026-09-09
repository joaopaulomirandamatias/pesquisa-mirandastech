#!/usr/bin/env python3
r"""Gera o acordo de orientação (expectativas mútuas) em Markdown para orientador e orientando preencherem juntos na primeira reunião.

    python3 scripts/acordo_orientacao.py --orientando "…" --orientador "…" --programa "…" --prazo AAAA-MM [--reunioes quinzenal|mensal|semanal] [--feedback 10] [--saida 00_projeto/ACORDO_ORIENTACAO.md]

Seções: papéis e responsabilidades (o que o orientador faz e não faz; o que o orientando faz); reuniões (frequência, duração, pauta, ata); feedback (prazo em dias para devolver texto, formato); marcos e prazos (qualificação, defesa, bolsa); autoria e crédito (critérios ICMJE, papéis CRediT, ordem de autoria decidida antes de escrever); dados, ética e integridade (CEP, LGPD, repositório); uso de IA (o que é permitido, como se declara — ligado ao manual de IA); comunicação e conflitos (canal, tempo de resposta, a quem recorrer); revisão do acordo. Campos «[preencher]» e regra: o acordo é revisto a cada marco e arquivado com data.
"""
import argparse, datetime, sys
from pathlib import Path

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--orientando", required=True); ap.add_argument("--orientador", required=True); ap.add_argument("--programa", default="[preencher]"); ap.add_argument("--prazo", required=True, help="AAAA-MM da defesa prevista")
    ap.add_argument("--reunioes", default="quinzenal", choices=["semanal", "quinzenal", "mensal"]); ap.add_argument("--feedback", type=int, default=10, help="dias úteis para devolver um texto"); ap.add_argument("--saida"); ap.add_argument("--forcar", action="store_true")
    a = ap.parse_args(); hoje = datetime.date.today().isoformat()
    S = [("1. Papéis", [f"Orientador(a) {a.orientador}: define com o orientando o plano de estudos, orienta o tema, o método e o texto, supervisiona o trabalho final e preside a banca (atribuições típicas dos regimentos); não escreve o texto pelo aluno nem decide sozinho a pergunta.",
                       f"Orientando(a) {a.orientando}: conduz a pesquisa, cumpre prazos combinados, traz pauta e texto para as reuniões, registra decisões, mantém o PROGRESSO.md e o diário de buscas.", "Coorientação: [há? quem? o que faz? formalizada no colegiado em …]"]),
         ("2. Reuniões", [f"Frequência: {a.reunioes}; duração: [preencher] min; quem marca: o orientando; pauta enviada [preencher] dia(s) antes; ata em REUNIOES.md (reuniao_orientacao.py) com decisões e próximos passos.", "Se uma reunião cai, remarca-se em até [preencher] dias; ausência sem aviso conta como pendência."]),
         ("3. Feedback", [f"Prazo para devolver um texto: até {a.feedback} dias úteis a partir do envio (o orientando avisa o tamanho e o que quer que seja lido).", "Formato: comentários no arquivo + três prioridades por rodada; o orientando responde a cada comentário (aceito/recusado, por quê).", "Texto entregue sem verificação de citações e referências volta sem leitura."]),
         ("4. Marcos e prazos", [f"Defesa prevista: {a.prazo}; qualificação: [preencher]; bolsa (agência, vigência, relatórios): [preencher]; estágio docência: [preencher].", "Cronograma em 00_projeto/CRONOGRAMA.md, revisto a cada marco."]),
         ("5. Autoria e crédito", ["Autoria pelos quatro critérios do ICMJE (contribuição substancial; redação ou revisão crítica; aprovação final; responsabilidade pelo todo); quem não cumpre os quatro vai aos agradecimentos.", "Papéis registrados com a taxonomia CRediT (autoria_credit.py) antes de escrever cada artigo; ordem de autoria decidida no início e revista se as contribuições mudarem; nem autoria honorária, nem fantasma.", "Chatbots não são autores; o uso de IA é declarado."]),
         ("6. Dados, ética e integridade", ["Pesquisa com pessoas: parecer do CEP (CAAE) antes da coleta; TCLE; LGPD; dado pessoal fora do repositório.", "Dados brutos intocados, com backup 3-2-1; scripts e decisões versionados; depósito com DOI ao final (plano de gestão de dados).", "Plágio, fabricação e falsificação: tolerância zero; dúvida se resolve antes, não depois."]),
         ("7. Uso de IA", ["O que é permitido (ex.: revisão gramatical, sugestão de estrutura, código com revisão humana) e o que não é (ex.: gerar dados, escrever resultados, resumir fontes que ninguém leu): [preencher conforme o manual de IA].", "Registro em USO_DE_IA.csv (ferramenta, fase, finalidade, validação); declaração no texto final."]),
         ("8. Comunicação e conflitos", ["Canal principal: [e-mail institucional / sistema do programa]; tempo de resposta esperado: [preencher] dias úteis; urgências: [preencher].", "Desacordo persistente: registrar em DECISOES.md; recorrer à coordenação/colegiado conforme o regimento; troca de orientador é prevista nos regimentos e não é falha de ninguém."]),
         ("9. Revisão deste acordo", [f"Assinado em {hoje}; revisto a cada marco (qualificação, fim da coleta, entrega); versões anteriores arquivadas com data."])]
    out = [f"# Acordo de orientação — {a.orientando} e {a.orientador}", f"Programa: {a.programa} · Rascunho gerado em {hoje} (modelo MirandasTech). Preencher juntos na primeira reunião; o regimento do programa prevalece.", ""]
    for t, itens in S: out += [f"## {t}"] + [f"- {i}" for i in itens] + [""]
    out += ["Assinaturas: ____________________ (orientando)   ____________________ (orientador)"]
    texto = "\n".join(out)
    if a.saida:
        p = Path(a.saida)
        if p.exists() and not a.forcar: sys.exit(f"{p} já existe — use --forcar")
        p.parent.mkdir(parents=True, exist_ok=True); p.write_text(texto, encoding="utf-8"); print(f"gravado: {p} ({len(S)} seções)")
    else: print(texto)

if __name__ == "__main__": main()
