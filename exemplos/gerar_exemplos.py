#!/usr/bin/env python3
"""Gera os dois projetos de exemplo (fictícios) em exemplos/: uma revisão sistemática na fase 6 e um estudo de caso na fase 8.
    python3 exemplos/gerar_exemplos.py    # recria exemplos/revisao-fase6 e exemplos/estudo-de-caso-fase8
Os arquivos mostram como fica um PROGRESSO.md preenchido com evidência; nomes, números e estudos são inventados."""
import re, shutil, subprocess, sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent; PLUGIN = AQUI.parent
AVISO = "\n> **Exemplo fictício** gerado por `exemplos/gerar_exemplos.py`: estudos, números e pessoas são inventados; serve para mostrar o formato preenchido.\n"

def projeto(pasta, **kw):
    if pasta.exists(): shutil.rmtree(pasta)
    args = [sys.executable, str(PLUGIN / "scripts/iniciar_projeto.py"), str(pasta)] + sum([[f"--{k}", v] for k, v in kw.items()], [])
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL); shutil.rmtree(pasta / ".git", ignore_errors=True)
    return pasta

def marcar(txt, chave, data, ev):
    pat = rf"^(\| {re.escape(chave)} \| [^|]+ \| [^|]+ \| [^|]+ \|) \[ \] \| \| \|$"
    novo, n = re.subn(pat, rf"\1 [x] | {data} | {ev} |", txt, count=1, flags=re.M); assert n == 1, chave; return novo

def escrever(p, s): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(s, encoding="utf-8")

# ---------------- Exemplo 1: revisão sistemática na fase 6 ----------------
p = projeto(AQUI / "revisao-fase6", tema="Manutenção preditiva com IA em terminais portuários", metodo="revisão sistemática", programa="PPGEE", prazo="2027-03")
t = (p / "PROGRESSO.md").read_text(encoding="utf-8")
for f, d, e in [("0", "2026-03-10", "cabeçalho; ACORDO_ORIENTADOR.md assinado"), ("1", "2026-03-24", "00_projeto/DECISOES_METODO.md §1–3"),
                ("2", "2026-04-07", "DECISOES_METODO.md §4–8; D003"), ("3", "2026-04-28", "06_texto/projeto_nbr15287.md; sem pessoas → CEP não se aplica (D004)"),
                ("4", "2026-05-19", "01_buscas/buscas.csv (3 bases); registro_exportacoes.csv com SHA-256; auditoria sem pendências críticas"),
                ("5", "2026-06-30", "02_triagem/prisma.md: 412 → 287 → 41 → 18 incluídos; κ = 0,81 (IC 0,72–0,90)")]: t = marcar(t, f, d, e)
for k, d, e in [("M1","2026-03-24","DECISOES_METODO.md §1"),("M2","2026-03-24","§2"),("M3","2026-03-24","§3 (duas revisões: Chen 2022; Okoro 2023)"),("M4","2026-06-30","01_buscas/; 04_sintese/matriz_sintese.csv em preenchimento"),
                ("M5","2026-04-07","§4"),("M6","2026-04-07","§5"),("M7","2026-04-07","§7 elegibilidade"),("M8","2026-04-07","§8 formulário de extração"),("M9","2026-04-28","D004: sem participantes humanos"),("M12","2026-04-28","06_texto/projeto_nbr15287.md"),
                ("I1","2026-04-14","ACORDO_ORIENTADOR.md; 00_protocolo/protocolo.md congelado em 2026-04-14"),("I2","2026-03-10","AGENTS.md"),("I3","2026-05-19","dados_FORA_DO_GIT/; hashes em registro_exportacoes.csv"),
                ("I4","2026-05-19","01_buscas/buscas.csv"),("I5","2026-05-12","01_buscas/teste_truncamento.md"),("I6","2026-06-02","05_analise/livro_de_codigos.csv v2; USO_DE_IA.csv linhas 1–3"),("I7","2026-06-30","02_triagem/kappa.md"),("I8","2026-07-14","02_triagem/texto_completo.md: 41 elegíveis, 39 obtidos, 2 E5"),
                ("B1","2026-03-17","item de teste 10.1016/j.jii.2023.100xxx importado"),("B2","2026-03-17","D005: sincronização + Storage"),("B3","2026-03-17","pasta de dados em ~/Zotero"),("B4","2026-03-17","ABNT testado com 3 tipos"),("B6","2026-04-07","tools/zotero_estrutura_colecoes.md"),("B7","2026-04-07","pesquisas salvas criadas"),("B8","2026-05-19","auditoria.csv sem críticas"),
                ("L1","2026-07-14","conta institucional (D006)"),("L2","2026-07-14","18 PDFs «Autor - Ano - Título» do Zotero"),("L3","2026-07-21","tools/inventario_notebook.md")]: t = marcar(t, k, d, e)
escrever(p / "PROGRESSO.md", t.replace("\n\n**Método provável:**", AVISO + "\n**Método provável:**", 1))
escrever(p / "00_projeto/DECISOES_METODO.md", f"""# Decisões de método — Manutenção preditiva com IA em terminais portuários
{AVISO}
## 1. Pergunta (2026-03-24)
Quais abordagens de inteligência artificial têm sido avaliadas para a manutenção preditiva de equipamentos em terminais portuários, e quais resultados e limitações são reportados?

## 2. Tabela vazia do resultado
| Estudo | Equipamento e contexto | Dados e tarefa | Abordagem de IA | Comparador | Validação | Resultados | Limitações |

## 3. Objetivos
Geral: sintetizar criticamente as evidências empíricas sobre abordagens de IA para manutenção preditiva em terminais portuários (2015–2026).
Específicos: (a) mapear equipamentos e tarefas; (b) comparar abordagens por tipo de dado; (c) identificar como os estudos validam e o que declaram como limitação.
Justificativa: as revisões de Chen (2022) e Okoro (2023) cobrem indústria de processo; nenhuma isola o contexto portuário.

## 4. Classificação (2026-04-07)
Natureza aplicada · abordagem qualitativa com síntese descritiva · objetivo exploratório · procedimento: revisão sistemática (PRISMA 2020).

## 5. Método
Escolhi revisão sistemática porque a pergunta é sobre o estado das evidências; descartei estudo de caso porque não há acesso a um terminal no prazo.

## 6. Análise
Síntese narrativa estruturada pela tabela do resultado; sem metanálise (heterogeneidade de métricas esperada).

## 7. Elegibilidade
Inclui: estudos empíricos 2015–2026, inglês/português, IA aplicada a manutenção preditiva de equipamento portuário. Exclui: revisões, editoriais, sem dados de equipamento.

## 8. Formulário de extração
As oito colunas da tabela do resultado + página da evidência + quem extraiu.
""")
escrever(p / "DECISOES.md", (p / "DECISOES.md").read_text(encoding="utf-8").replace("**Data:** AAAA-MM-DD · **Responsável:** … · **Decisão:** … · **Justificativa:** … · **Impacto medido:** …",
 "**Data:** 2026-04-07 · **Responsável:** autor · **Decisão:** Scopus, Web of Science e IEEE Xplore · **Justificativa:** cobertura de engenharia e computação · **Impacto medido:** 412 registros brutos, 287 após deduplicação")
 .replace("**Data:** … · **Partes:** autor e orientador · **Permitido:** … · **Vedado:** … · **Declaração:** … · **Ferramentas e configuração:** …",
 "**Data:** 2026-04-14 · **Partes:** autor e orientador (M. Andrade) · **Permitido:** sugestão de termos de busca, ordenação da triagem com status preliminar, revisão gramatical · **Vedado:** decidir inclusão, extrair sem conferência no PDF, redigir resultados · **Declaração:** seção «Uso de IA» no capítulo de método · **Ferramentas e configuração:** Claude Code (treinamento desligado), Gemini Notebook em conta institucional")
 + "\n## D003 — Revisão sistemática sem metanálise\n**Data:** 2026-04-07 · **Responsável:** autor e orientador · **Decisão:** síntese narrativa · **Justificativa:** métricas heterogêneas · **Impacto medido:** —\n\n## D004 — Sem submissão ao CEP\n**Data:** 2026-04-28 · **Responsável:** autor e orientador · **Decisão:** revisão sem participantes humanos; CEP não se aplica · **Justificativa:** Res. CNS 510/2016, art. 1º · **Impacto medido:** fase 3 fechada sem espera de parecer\n\n## D005 — Sincronização e arquivos no Zotero\n**Data:** 2026-03-17 · **Responsável:** autor · **Decisão:** sincronização automática; arquivos no Zotero Storage · **Justificativa:** biblioteca < 300 MB · **Impacto medido:** —\n\n## D006 — Conta do Gemini Notebook\n**Data:** 2026-07-14 · **Responsável:** autor · **Decisão:** conta institucional · **Justificativa:** política de privacidade (sem revisão humana) · **Impacto medido:** —\n" + AVISO)
escrever(p / "USO_DE_IA.csv", (p / "USO_DE_IA.csv").read_text(encoding="utf-8") +
 '2026-05-05,busca,Claude Code,claude-sonnet-5,sugerir sinônimos para a string,termos da pergunta,"proponha variantes de manutenção preditiva e terminal portuário",string final decidida pelo autor e testada nas 3 bases,sim,declare,autor\n'
 '2026-06-02,triagem,Claude Code,claude-sonnet-5,agrupar 287 registros pelo livro de códigos v2 com status preliminar,títulos e identificadores; resumos locais,"aplicar R1–R6; não decidir",autor decidiu um a um; 41 elegíveis,sim por registro,declare,autor\n'
 '2026-07-21,leitura,Gemini Notebook,Gemini 3.5,inventário das 18 fontes e perguntas por seção,18 PDFs licenciados (conta institucional),"para cada fonte: objetivo; método; resultado; limitação com citação",cada célula conferida no trecho citado,sim,declare,autor\n')
escrever(p / "01_buscas/buscas.csv", (p / "01_buscas/buscas.csv").read_text(encoding="utf-8") +
 '2026-05-19,Scopus,"TITLE-ABS-KEY((""predictive maintenance"" OR ""condition-based maintenance"") AND (port OR terminal OR crane) AND (""machine learning"" OR ""deep learning"" OR ""artificial intelligence""))","2015-2026; article; conference paper",203,scopus_2026-05-19.csv,<sha256>\n'
 '2026-05-19,Web of Science,"TS=((""predictive maintenance"") AND (port* OR terminal* OR crane*) AND (""machine learning"" OR ""deep learning""))","2015-2026; Article; Proceedings",141,wos_2026-05-19.txt,<sha256>\n'
 '2026-05-19,IEEE Xplore,"(""predictive maintenance"") AND (port OR crane) AND (""machine learning"")","2015-2026",68,ieee_2026-05-19.csv,<sha256>\n')
escrever(p / "02_triagem/prisma.md", f"# Números do PRISMA 2020\n{AVISO}\n| Etapa | n |\n|---|---|\n| Registros identificados (3 bases) | 412 |\n| Após deduplicação (Zotero) | 287 |\n| Excluídos na triagem de título e resumo | 246 |\n| Elegíveis para texto completo | 41 |\n| Texto completo obtido | 39 (2 não obtidos: E5) |\n| Excluídos no texto completo | 21 (sem equipamento portuário: 14; sem dados: 7) |\n| Incluídos | 18 |\n\nConcordância entre revisores na amostra de 60: κ = 0,81 (IC 95% 0,72–0,90).\n")
escrever(p / "04_sintese/matriz_sintese.csv", (p / "04_sintese/matriz_sintese.csv").read_text(encoding="utf-8") +
 'E01,Almeida 2023,LSTM prevê falha em guindaste STS?,terminal de contêineres (fictício),experimento,3 guindastes,vibração e corrente,F1 0.91 em janela de 24 h,sem custo medido,dado de um terminal só,p. 7\n'
 'E02,Nakamura 2021,Random forest para RTG?,pátio de contêineres,estudo de caso,12 RTG,sensores hidráulicos,redução de 12% das paradas não programadas,sem comparador,p. 12\n'
 'E03,Duarte 2024,Detecção de anomalia em esteira de granéis?,terminal de grãos,experimento,1 linha,acústica,AUC 0.88,validação em 2 meses,p. 5\n')
escrever(p / "README.md", f"# Exemplo: revisão sistemática na fase 6\n{AVISO}\nO que mostra: fases 0–5 fechadas com evidência, fase 6 (leitura e síntese) aberta com a matriz em preenchimento, decisões D001–D006 datadas, três usos de IA registrados, números do PRISMA e três buscas com string verbatim. Abra o Claude Code aqui e diga «Pesquisador, onde paramos?».\n")

# ---------------- Exemplo 2: estudo de caso na fase 8 ----------------
p = projeto(AQUI / "estudo-de-caso-fase8", tema="Adoção de gêmeo digital na operação de um terminal de contêineres", metodo="estudo de caso", programa="PPGEP", prazo="2026-12")
t = (p / "PROGRESSO.md").read_text(encoding="utf-8")
for f, d, e in [("0","2025-09-08","cabeçalho; acordo assinado"),("1","2025-09-22","DECISOES_METODO.md §1–3"),("2","2025-10-13","§4–8; D003"),("3","2025-12-15","projeto NBR 15287; parecer CEP CAAE 00000000.0.0000.0000 (D004)"),
                ("4","2026-02-02","buscas.csv; biblioteca auditada"),("5","2026-02-23","triagem de 96 → 22 documentos internos e artigos de apoio"),("6","2026-04-06","matriz_sintese.csv 22 linhas conferidas"),("7","2026-07-13","05_analise/: 14 entrevistas transcritas e codificadas (livro de códigos v3); dados em dados_FORA_DO_GIT")]: t = marcar(t, f, d, e)
for k, d, e in [("M1","2025-09-22","§1"),("M2","2025-09-22","§2"),("M3","2025-09-22","§3"),("M4","2026-04-06","matriz_sintese.csv"),("M5","2025-10-13","§4"),("M6","2025-10-13","§5"),("M7","2025-10-13","§7: 14 entrevistados por papel (saturação em 12)"),("M8","2025-10-13","02_instrumentos/roteiro_entrevista.md; pré-teste com 2"),
                ("M9","2025-12-15","03_etica/parecer_cep.pdf (fora do git); TCLE arquivado"),("M10","2026-07-13","análise temática (Braun & Clarke) decidida em §6"),("M11","2026-07-13","05_analise/scripts/; figuras por script"),("M12","2025-12-15","06_texto/projeto_nbr15287.md"),
                ("I1","2025-10-20","acordo; protocolo congelado"),("I2","2025-09-08","AGENTS.md"),("I3","2026-07-13","transcrições anonimizadas em dados_FORA_DO_GIT"),("I9","2026-07-13","codificação com página e trecho; dupla codificação em 20%"),("I10","2026-07-20","figuras geradas por 05_analise/scripts/figuras.py"),
                ("B1","2025-09-15","testado"),("B4","2025-09-15","ABNT"),("B6","2025-10-13","coleções por etapa"),("B8","2026-02-02","auditoria sem críticas"),("L1","2026-03-02","conta institucional"),("L2","2026-03-02","22 fontes"),("L4","2026-04-06","trechos conferidos"),("L5","2026-04-06","matriz conferida célula a célula")]: t = marcar(t, k, d, e)
escrever(p / "PROGRESSO.md", t.replace("\n\n**Método provável:**", AVISO + "\n**Método provável:**", 1))
escrever(p / "00_projeto/DECISOES_METODO.md", f"# Decisões de método — gêmeo digital num terminal de contêineres\n{AVISO}\n## 1. Pergunta (2025-09-22)\nComo a adoção de um gêmeo digital altera as práticas de planejamento operacional de um terminal de contêineres, na percepção dos planejadores e supervisores?\n\n## 2. Tabela vazia do resultado\n| Prática | Antes do gêmeo digital | Depois | Quem relata | Evidência (entrevista, documento) |\n\n## 3. Objetivos\nGeral: compreender as mudanças nas práticas de planejamento após a adoção do gêmeo digital num terminal (caso único).\n\n## 4. Classificação (2025-10-13)\nAplicada · qualitativa · exploratória-descritiva · estudo de caso único (Yin) com entrevistas e documentos.\n\n## 5. Método\nEscolhi estudo de caso porque a pergunta é «como» num contexto real; descartei survey porque a população é pequena e o fenômeno é recente.\n\n## 6. Análise\nAnálise temática (Braun & Clarke) com livro de códigos versionado; dupla codificação em 20% das entrevistas.\n\n## 7. Amostra\n14 entrevistados por papel (planejadores, supervisores, TI); saturação observada na 12ª.\n\n## 8. Instrumento\nRoteiro semiestruturado (02_instrumentos/roteiro_entrevista.md), pré-testado com 2 participantes.\n")
escrever(p / "DECISOES.md", (p / "DECISOES.md").read_text(encoding="utf-8").replace("**Data:** AAAA-MM-DD · **Responsável:** … · **Decisão:** … · **Justificativa:** … · **Impacto medido:** …",
 "**Data:** 2026-01-19 · **Responsável:** autor · **Decisão:** Scopus e Web of Science para a literatura de apoio; documentos internos do terminal por autorização escrita · **Justificativa:** o caso é a fonte principal · **Impacto medido:** 96 documentos e artigos triados")
 .replace("**Data:** … · **Partes:** autor e orientador · **Permitido:** … · **Vedado:** … · **Declaração:** … · **Ferramentas e configuração:** …",
 "**Data:** 2025-10-20 · **Partes:** autor e orientadora (L. Ferreira) · **Permitido:** transcrição bruta conferida; sugestão de códigos com status preliminar; revisão gramatical · **Vedado:** enviar transcrições identificáveis; interpretar temas; redigir resultados · **Declaração:** seção no capítulo de método · **Ferramentas e configuração:** Claude Code; Gemini Notebook institucional")
 + "\n## D003 — Estudo de caso único\n**Data:** 2025-10-13 · **Responsável:** autor e orientadora · **Decisão:** caso único, terminal X · **Justificativa:** acesso autorizado e fenômeno recente · **Impacto medido:** —\n\n## D004 — Submissão ao CEP\n**Data:** 2025-12-15 · **Responsável:** autor · **Decisão:** submetido pela Plataforma Brasil; parecer favorável CAAE 00000000.0.0000.0000 (fictício) · **Justificativa:** entrevistas com pessoas · **Impacto medido:** coleta iniciada em 2026-03\n" + AVISO)
escrever(p / "USO_DE_IA.csv", (p / "USO_DE_IA.csv").read_text(encoding="utf-8") +
 '2026-03-16,coleta,Whisper local,large-v3,transcrição bruta de 14 entrevistas,áudio anonimizado (sem nomes),"transcrever",cada transcrição conferida com o áudio pelo autor,sim,declare,autor\n'
 '2026-05-04,analise,Claude Code,claude-sonnet-5,sugerir códigos iniciais a partir de 3 transcrições anonimizadas,3 transcrições sem identificadores,"proponha códigos descritivos; não interprete",autor manteve 9 de 17 sugestões; livro de códigos v1,sim,declare,autor\n')
escrever(p / "05_analise/livro_de_codigos.csv", (p / "05_analise/livro_de_codigos.csv").read_text(encoding="utf-8") +
 'C01,Planejamento por simulação,Uso do gêmeo para testar cenários antes de decidir,Menções a «rodar o cenário» antes da decisão,Decisão sem simulação,E03 l. 41\nC02,Confiança no modelo,Julgamentos sobre acreditar ou não na previsão,Dúvida ou confiança explícita,Descrição técnica sem juízo,E07 l. 112\n')
escrever(p / "README.md", f"# Exemplo: estudo de caso na fase 8\n{AVISO}\nO que mostra: fases 0–7 fechadas (inclusive CEP e coleta), fase 8 (escrita ABNT) aberta, decisões D001–D004, usos de IA na transcrição e na codificação, livro de códigos com dois códigos. Abra o Claude Code aqui e diga «Pesquisador, onde paramos?».\n")
print("exemplos gerados")
