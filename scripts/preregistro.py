#!/usr/bin/env python3
r"""Gera o rascunho do pré-registro do estudo em Markdown, com as perguntas do modelo escolhido, para o aluno preencher e colar no OSF ou no AsPredicted.

    python3 scripts/preregistro.py --modelo aspredicted|osf|revisao --titulo "…" [--saida 00_protocolo/PREREGISTRO.md]

Modelos (perguntas transcritas em português, com o nome original entre parênteses):
- aspredicted: as oito perguntas do formulário AsPredicted (dados existentes, hipótese, variável dependente, condições, análises, outliers/exclusões, tamanho da amostra, outros).
- osf: as seções do «OSF Preregistration» (informações do estudo, desenho, plano de amostragem, variáveis, plano de análise).
- revisao: as seções de um pré-registro de revisão sistemática no padrão PROSPERO/PRISMA-P (pergunta, critérios, fontes, estratégia, seleção, extração, risco de viés, síntese).
O arquivo sai com campos «[preencher]» e com a regra de que, uma vez registrado, o texto não muda — mudanças viram emenda datada.
"""
import argparse, datetime, sys
from pathlib import Path

ASPREDICTED = [("Dados existentes (Data collection)", "Já foi coletado algum dado para este estudo? Responda: ainda não; sim, mas não foi visto; sim, já foi visto — e explique."),
 ("Hipótese (Hypothesis)", "Qual é a pergunta principal ou a hipótese testada? Uma frase, direcional se houver expectativa."),
 ("Variável dependente (Dependent variable)", "Descreva a(s) variável(is) de resultado, como será(ão) medida(s) e a unidade."),
 ("Condições (Conditions)", "Quantas e quais condições/grupos os participantes ou casos terão? Como serão alocados?"),
 ("Análises (Analyses)", "Especifique exatamente qual análise testará a hipótese principal (teste, modelo, variáveis, covariáveis, nível de significância ou critério bayesiano)."),
 ("Exclusões e outliers (Outliers and exclusions)", "Regras para excluir observações ou participantes, decididas antes de ver os dados."),
 ("Tamanho da amostra (Sample size)", "Quantas observações serão coletadas e a regra de parada; justifique (cálculo de poder, recursos, precisão)."),
 ("Outros (Other)", "Qualquer outra coisa que você queira pré-registrar (análises secundárias, variáveis adicionais, planos para dados faltantes).")]
OSF = [("Informações do estudo (Study Information)", "Título; autores; descrição; hipóteses (cada uma numerada e, se possível, direcional)."),
 ("Desenho (Design Plan)", "Tipo de estudo (experimental, observacional, meta-análise, outro); cegamento; desenho (entre/intra-sujeitos, fatores); randomização."),
 ("Plano de amostragem (Sampling Plan)", "Dados já existentes? procedimento de coleta; tamanho da amostra; justificativa do tamanho; regra de parada."),
 ("Variáveis (Variables)", "Variáveis manipuladas; variáveis medidas; índices/escores derivados (como serão calculados)."),
 ("Plano de análise (Analysis Plan)", "Modelos estatísticos por hipótese; transformações; inferência (α, IC, critério bayesiano); dados faltantes; exclusões; análises exploratórias declaradas como tal.")]
REVISAO = [("Título e registro", "Título da revisão; registro (PROSPERO, OSF Registries); autores e contato; fontes de financiamento e conflitos."),
 ("Pergunta (PICO/PEO/SPIDER)", "População, intervenção/exposição, comparação, desfechos; ou o formato adequado ao tipo de revisão."),
 ("Critérios de elegibilidade", "Tipos de estudo, participantes, intervenções, desfechos, idioma, período, tipo de publicação — inclusão e exclusão."),
 ("Fontes de informação", "Bases (nome e plataforma), registros de ensaios, literatura cinzenta, contato com autores, snowballing; data prevista das buscas."),
 ("Estratégia de busca", "String completa de pelo menos uma base (verbatim), limites e filtros; quem desenhou; revisão por pares (PRESS)."),
 ("Seleção dos estudos", "Quantos revisores, independência, cegamento, ferramenta (ASReview, Rayyan…), resolução de discordâncias, medida de concordância."),
 ("Extração de dados", "Formulário, itens, quem extrai, pilotagem, contato com autores para dados faltantes."),
 ("Risco de viés / qualidade", "Instrumento (RoB 2, ROBINS-I, JBI, CASP…), por desfecho ou por estudo, quem avalia."),
 ("Síntese", "Critérios para meta-análise ou síntese narrativa; medidas de efeito; heterogeneidade; análises de subgrupo/sensibilidade; viés de publicação; certeza da evidência (GRADE)."),
 ("Emendas", "Como mudanças no protocolo serão registradas (data, o que mudou, por quê).")]

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--modelo", choices=["aspredicted", "osf", "revisao"], required=True); ap.add_argument("--titulo", required=True)
    ap.add_argument("--autores", default="[preencher]"); ap.add_argument("--saida", default=None); ap.add_argument("--forcar", action="store_true")
    a = ap.parse_args(); itens = {"aspredicted": ASPREDICTED, "osf": OSF, "revisao": REVISAO}[a.modelo]
    nome = {"aspredicted": "AsPredicted (8 perguntas)", "osf": "OSF Preregistration", "revisao": "Revisão sistemática (PROSPERO / PRISMA-P)"}[a.modelo]
    hoje = datetime.date.today().isoformat()
    out = [f"# Pré-registro — {a.titulo}", f"Modelo: {nome} · Rascunho gerado em {hoje} · Autores: {a.autores}", "",
           "> Regra: o texto registrado não muda. Preencha tudo antes de coletar (ou antes de extrair, numa revisão). Depois de registrado, qualquer mudança é uma emenda datada, com o motivo, registrada no mesmo lugar e no DECISOES.md.", ""]
    for i, (t, d) in enumerate(itens, start=1): out += [f"## {i}. {t}", f"_{d}_", "", "[preencher]", ""]
    out += ["## Onde registrar", "- OSF: My Registrations → Add a Registration → escolher o modelo → preencher → Register (público ou embargo de até 4 anos) → DOI permanente.",
            "- AsPredicted: New Pre-registration → 8 perguntas → PDF com data e URL única (privado até você tornar público).",
            "- Revisão sistemática em saúde: PROSPERO (gratuito; antes da extração de dados). Outras revisões: OSF Registries (modelo Systematic Review).", ""]
    texto = "\n".join(out)
    if a.saida:
        p = Path(a.saida)
        if p.exists() and not a.forcar: sys.exit(f"{p} já existe — use --forcar para sobrescrever")
        p.parent.mkdir(parents=True, exist_ok=True); p.write_text(texto, encoding="utf-8"); print(f"gravado: {p} ({len(itens)} seções, modelo {a.modelo})")
    else: print(texto)

if __name__ == "__main__": main()
