#!/usr/bin/env bash
# Prepara, na pasta de trabalho do caso (cwd), um projeto criado pelo iniciar_projeto.py e aplica um cenário.
# Uso: projeto.sh <cenario>   cenários: fase0 | fase1-aberta | fase3 | material-posterior
set -e
PLUGIN="$(cd "$(dirname "$0")/../.." && pwd)"
python3 "$PLUGIN/scripts/iniciar_projeto.py" . --tema "Manutenção preditiva com IA em terminais portuários" --metodo "revisão sistemática" --programa "PPGEE" --prazo 2027-03 >/dev/null
python3 - "$1" <<'PY'
import sys, re
cen = sys.argv[1]; p = "PROGRESSO.md"; t = open(p, encoding="utf-8").read()
def fechar_fase(n, data, ev):
    global t
    t = re.sub(rf"^(\| {n} \| [^|]+ \| [^|]+ \| [^|]+ \|) \[ \] \| \| \|$", rf"\1 [x] | {data} | {ev} |", t, count=1, flags=re.M)
def fechar_item(k, data, ev):
    global t
    t = re.sub(rf"^(\| {k} \| [^|]+ \| [^|]+ \| [^|]+ \|) \[ \] \| \| \|$", rf"\1 [x] | {data} | {ev} |", t, count=1, flags=re.M)
if cen in ("fase1-aberta", "fase3", "material-posterior"):
    fechar_fase(0, "2026-08-20", "cabeçalho do PROGRESSO.md; ACORDO_ORIENTADOR.md assinado")
    open("ACORDO_ORIENTADOR.md", "a", encoding="utf-8").write("\n\nAssinado em 2026-08-20 por autor e orientador (J. Silva).\n")
if cen == "fase3":
    fechar_fase(1, "2026-08-27", "00_projeto/DECISOES_METODO.md §1–3 (pergunta, tabela vazia, objetivos)")
    fechar_fase(2, "2026-09-03", "00_projeto/DECISOES_METODO.md §4–6; DECISOES.md D003")
    for k, d, e in [("M1", "2026-08-27", "DECISOES_METODO.md §1"), ("M2", "2026-08-27", "DECISOES_METODO.md §2"), ("M3", "2026-08-27", "DECISOES_METODO.md §3"),
                    ("M5", "2026-09-03", "DECISOES_METODO.md §4"), ("M6", "2026-09-03", "DECISOES_METODO.md §5"),
                    ("M7", "2026-09-03", "DECISOES_METODO.md §7 (critérios de elegibilidade = população da revisão)"), ("M8", "2026-09-03", "DECISOES_METODO.md §8 (formulário de extração)"), ("I1", "2026-08-20", "ACORDO_ORIENTADOR.md")]:
        fechar_item(k, d, e)
    open("00_projeto/DECISOES_METODO.md", "w", encoding="utf-8").write("""# Decisões de método

## 1. Pergunta (2026-08-27)
Quais abordagens de inteligência artificial têm sido avaliadas para a manutenção preditiva de equipamentos em terminais portuários, e quais resultados e limitações são reportados?

## 2. Tabela vazia do resultado
| Estudo | Equipamento e contexto | Dados e tarefa | Abordagem de IA | Comparador | Validação | Resultados | Limitações |

## 3. Objetivos
Geral: sintetizar criticamente as evidências empíricas sobre abordagens de IA para manutenção preditiva em terminais portuários.
Específicos: mapear as aplicações; comparar resultados por tipo de equipamento; identificar limitações reportadas.

## 4. Classificação (2026-09-03)
Natureza aplicada; abordagem qualitativa com síntese descritiva; objetivo exploratório; procedimento: revisão sistemática.

## 5. Método
Escolhi revisão sistemática porque a pergunta é sobre o estado das evidências; descartei estudo de caso porque não há acesso a um terminal.

## 6. Análise
Síntese narrativa estruturada pela tabela do resultado; sem metanálise (heterogeneidade esperada).

## 7. Elegibilidade (o «quem» da revisão)
Inclui: estudos empíricos, 2015–2026, em inglês ou português, com abordagem de IA aplicada a manutenção preditiva de equipamento portuário. Exclui: revisões, editoriais, estudos sem dados de equipamento.

## 8. Formulário de extração
As oito colunas da tabela vazia do resultado, mais «página da evidência» e «quem extraiu».
""")
    d = open("DECISOES.md", encoding="utf-8").read()
    d = d.replace("**Data:** AAAA-MM-DD · **Responsável:** … · **Decisão:** … · **Justificativa:** … · **Impacto medido:** …",
                  "**Data:** 2026-08-27 · **Responsável:** autor · **Decisão:** Scopus, Web of Science e IEEE Xplore · **Justificativa:** cobertura de engenharia · **Impacto medido:** a medir na fase 4")
    d += "\n## D003 — Revisão sistemática sem metanálise\n**Data:** 2026-09-03 · **Responsável:** autor e orientador · **Decisão:** síntese narrativa · **Justificativa:** heterogeneidade esperada · **Impacto medido:** —\n"
    open("DECISOES.md", "w", encoding="utf-8").write(d)
if cen == "material-posterior":
    open("04_sintese/matriz_sintese.csv", "a", encoding="utf-8").write(
        "E01,Silva 2023,IA reduz paradas?,terminal de contêineres,estudo de caso,1 terminal,sensores,redução de 12% nas paradas,sem comparador,p. 7\n"
        "E02,Souza 2024,LSTM prevê falha?,guindaste STS,experimento,3 equipamentos,vibração,F1 0,91,sem custo medido,p. 12\n")
open(p, "w", encoding="utf-8").write(t)
PY
