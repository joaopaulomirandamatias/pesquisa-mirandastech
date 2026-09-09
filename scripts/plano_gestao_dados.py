#!/usr/bin/env python3
r"""Gera o Plano de Gestão de Dados (PGD/DMP) do projeto em Markdown, com as seções usuais das agências e do DMPTool, para o aluno preencher.

    python3 scripts/plano_gestao_dados.py --titulo "…" [--saida 00_projeto/PLANO_GESTAO_DADOS.md] [--repositorio Zenodo] [--licenca CC-BY-4.0]

Seções: descrição dos dados (tipos, formatos, volume); documentação e metadados (README, dicionário de dados, padrão da área); ética e dados pessoais (LGPD, TCLE, anonimização, o que não será compartilhado); armazenamento e backup durante o projeto (3-2-1); compartilhamento e preservação (repositório, DOI, licença, embargo, quando); responsabilidades e custos; cronograma de revisão do plano.
"""
import argparse, datetime, sys
from pathlib import Path

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--titulo", required=True); ap.add_argument("--saida"); ap.add_argument("--repositorio", default="Zenodo"); ap.add_argument("--licenca", default="CC-BY-4.0"); ap.add_argument("--forcar", action="store_true")
    a = ap.parse_args(); hoje = datetime.date.today().isoformat()
    S = [("1. Descrição dos dados", ["Que dados serão coletados ou reutilizados (entrevistas, planilhas de medições, logs de sensores, imagens…)?", "Formatos na coleta e na entrega (preferir abertos: csv, txt, json, ods, pdf/A, png).", "Volume estimado (MB/GB) e número de arquivos.", "Dados reutilizados: fonte, licença, DOI."]),
         ("2. Documentação e metadados", ["README por conjunto: o que é, como foi coletado, quando, por quem, com que instrumento.", "Dicionário de dados: cada variável com nome, tipo, unidade, valores possíveis, ausentes.", "Padrão de metadados da área, se houver (ex.: Dublin Core, DDI, ISO 19115).", "Nomes de arquivo previsíveis: AAAA-MM-DD_projeto_conteudo_v01.ext."]),
         ("3. Ética, dados pessoais e sigilo", ["Há dados pessoais ou sensíveis (LGPD)? Quais? Base legal e TCLE (o que o participante autorizou compartilhar).", "Anonimização/pseudonimização: método, quando, quem; chave guardada fora do repositório.", "Dados licenciados de terceiros (bases pagas, resumos): ficam fora do repositório público.", "O que NÃO será compartilhado e por quê (com a alternativa: metadados, dados agregados, acesso mediado)."]),
         ("4. Armazenamento e backup durante o projeto", ["Regra 3-2-1: três cópias, dois suportes, uma fora do local (ex.: máquina + nuvem institucional + HD externo).", "Controle de versão do código e dos derivados (Git); dado bruto intocado e somente leitura.", "Quem tem acesso; criptografia para dados sensíveis."]),
         ("5. Compartilhamento e preservação", [f"Repositório: {a.repositorio} (DOI; conferir no re3data se há repositório da área ou da instituição).", f"Licença: {a.licenca} para dados e texto; código com licença de software (MIT/Apache/GPL).", "Quando: ao publicar o artigo / na defesa; embargo se necessário (motivo e prazo).", "Versão congelada: tag no Git + release + DOI de versão; o DOI de conceito no texto."]),
         ("6. Responsabilidades e custos", ["Quem cuida dos dados durante e depois do projeto; o que acontece se a pessoa sair.", "Custos (armazenamento, anonimização, curadoria) e fonte."]),
         ("7. Revisão do plano", [f"Plano criado em {hoje}; revisar a cada marco (qualificação, fim da coleta, defesa) e registrar as mudanças com data."])]
    out = [f"# Plano de Gestão de Dados — {a.titulo}", f"Rascunho gerado em {hoje} (modelo MirandasTech; seções compatíveis com o DMPTool e com os PGDs pedidos por agências).", ""]
    for t, itens in S: out += [f"## {t}"] + [f"- {i}\n  - [preencher]" for i in itens] + [""]
    texto = "\n".join(out)
    if a.saida:
        p = Path(a.saida)
        if p.exists() and not a.forcar: sys.exit(f"{p} já existe — use --forcar")
        p.parent.mkdir(parents=True, exist_ok=True); p.write_text(texto, encoding="utf-8"); print(f"gravado: {p} ({len(S)} seções)")
    else: print(texto)

if __name__ == "__main__": main()
