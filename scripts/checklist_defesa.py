#!/usr/bin/env python3
r"""Gera o checklist da qualificação ou da defesa em Markdown, com prazos contados a partir da data marcada, para o aluno conferir com o regimento do programa.

    python3 scripts/checklist_defesa.py --data AAAA-MM-DD --tipo qualificacao|defesa [--saida 07_banca/CHECKLIST_DEFESA.md]

Cada item traz «quando» (dias antes/depois, a confirmar no regimento — os prazos variam por programa), «o quê» e «evidência». Blocos: antes (texto, banca, agendamento, documentos, apresentação, ensaio), no dia (material, sala/link, tempo, arguição) e depois (ata, correções, versão final, depósito, diploma). Não substitui o regimento: cada linha tem espaço para o prazo oficial.
"""
import argparse, datetime, sys
from pathlib import Path

ANTES = [(-90, "Confirmar no regimento: prazos, composição da banca, tempo de apresentação e arguição, formato (presencial/remoto)", "página do regimento salva em 07_banca/"),
         (-60, "Texto completo revisado (citações e referências verificadas; números batem com as tabelas); banca sugerida ao orientador", "verificar_citacoes.py e verificar_refs.py sem erro"),
         (-45, "Banca aprovada pelo programa; data, hora e sala/link definidos com todos os membros", "e-mail de confirmação de cada membro"),
         (-30, "Texto entregue à banca (PDF e impresso se o regimento pedir) com os documentos exigidos pela secretaria", "protocolo de entrega"),
         (-21, "Apresentação pronta (apresentacao_defesa.py): um resultado por slide, tempo por bloco, referências", "PDF da apresentação"),
         (-14, "Banca simulada: as cinco objeções mais fortes e as respostas honestas; o que corrigir no texto", "06_texto/banca.md"),
         (-7, "Três ensaios cronometrados (ensaio_defesa.py) — o último com público", "ensaio.csv"),
         (-2, "Material impresso: texto anotado, lista de números-chave, tabelas principais; testar projetor/PDF/link", "pasta 07_banca/dia/")]
DIA = [(0, "Chegar cedo; PDF em dois lugares (pendrive e nuvem); água; relógio visível", "—"),
       (0, "Apresentar no tempo; anotar cada pergunta antes de responder; conceder o que for procedente", "anotações da arguição"),
       (0, "Ouvir o parecer e a ata; registrar todas as correções pedidas", "lista de correções")]
DEPOIS = [(7, "Lista de correções acordada com o orientador; o que muda no texto e o que só se responde", "07_banca/CORRECOES.md"),
          (30, "Versão corrigida enviada ao orientador (e à banca, se o regimento exigir)", "PDF v-final-candidata"),
          (60, "Depósito da versão final na biblioteca/repositório institucional conforme o regimento; dados e código com DOI se previsto", "recibo de depósito"),
          (90, "Diploma/certificado: acompanhar a solicitação na secretaria", "protocolo")]

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", required=True); ap.add_argument("--tipo", choices=["qualificacao", "defesa"], required=True); ap.add_argument("--saida"); ap.add_argument("--forcar", action="store_true")
    a = ap.parse_args(); d0 = datetime.date.fromisoformat(a.data); ev = "Exame de qualificação" if a.tipo == "qualificacao" else "Defesa"
    def bloco(titulo, itens):
        out = [f"## {titulo}", "| Quando (sugerido) | Prazo do regimento | O quê | Evidência | Feito |", "|---|---|---|---|---|"]
        for dias, oque, ev_ in itens:
            data = d0 + datetime.timedelta(days=dias); q = f"{data.isoformat()} ({dias:+d} d)" if dias else data.isoformat()
            out.append(f"| {q} | [conferir] | {oque} | {ev_} | [ ] |")
        return out + [""]
    out = [f"# Checklist — {ev} em {d0.isoformat()}", "Prazos sugeridos a partir da data marcada; **o regimento do programa prevalece** — preencha a coluna «Prazo do regimento».", ""]
    if a.tipo == "qualificacao": DEPOIS[2] = (60, "Incorporar as sugestões da banca ao plano até a defesa; atualizar cronograma e PROGRESSO.md", "PROGRESSO.md")
    out += bloco("Antes", ANTES) + bloco("No dia", DIA) + bloco("Depois", DEPOIS)
    texto = "\n".join(out)
    if a.saida:
        p = Path(a.saida)
        if p.exists() and not a.forcar: sys.exit(f"{p} já existe — use --forcar")
        p.parent.mkdir(parents=True, exist_ok=True); p.write_text(texto, encoding="utf-8"); print(f"gravado: {p} ({len(ANTES)+len(DIA)+len(DEPOIS)} itens)")
    else: print(texto)

if __name__ == "__main__": main()
