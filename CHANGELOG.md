# Histórico de versões

## 1.0.16 — 2026-10-13
- `plano_de_ensino.py`: o cronograma padrão passa a 17 semanas (`--semanas 17`). As semanas 1 a 15 não mudam; a 16 é a submissão do artigo (manual de Submissão: `CHECKLIST_SUBMISSAO.md`, `CARTA_APRESENTACAO.md`) e a 17 o estágio de docência (manual do professor: semana conduzida sob supervisão, rubrica com `rubrica.py`). Ementa gerada atualizada. Execução real: «gravado: PLANO_DE_ENSINO.md (17 semanas, 17 fases cobertas)».
- `ensino-pesquisa`: cronograma padrão de 17 semanas e o comando com `--semanas 17`.

## 1.0.15 — 2026-10-13
- `revisao-sistematica-prisma`: a decisão de usar IA entra já no protocolo (declaração conjunta Cochrane, Campbell, JBI e CEE, 2025, https://doi.org/10.11124/JBIES-25-00480); ao definir o limiar do ASReview, o aluno é avisado de que o RAISE 3 (v.4, 23/09/2026, rascunho em revisão, https://osf.io/fwaud/) classifica a triagem priorizada com parada antecipada como «Requires validation within the review»; relato pelo item 4.9 do RAISE 1; PRISMA-trAIce só como lista de conferência, sem endosso da direção do PRISMA (Moher et al., 2026, https://doi.org/10.2196/104210); nova recusa: LLM sintetizando achados entre estudos («not acceptable» no RAISE 3).
- `triagem-assistida`: antes do lote inteiro, as propostas da IA são validadas num subconjunto da própria revisão, com limiar definido antes (RAISE 3, Tabela 2: LLM na triagem = «Requires validation within the review»).
- Manual do plugin (https://plugin.mirandastech.com.br/) no padrão visual do site e do blog: tela escura, Geist, Geist Mono e Instrument Serif, cabeçalho e rodapé da marca, Laboratório em https://lab.mirandastech.com.br/; o PDF continua claro.

## 1.0.14 — 2026-09-09
- Nova skill `submissao-orcid-lattes`: escolha do periódico (Think. Check. Submit., Qualis na Sucupira, DOAJ, COPE, Open policy finder), checklist de submissão com evidência, carta de apresentação, resposta ponto a ponto aos revisores, ORCID e Lattes coerentes, ligada ao manual https://submissao.mirandastech.com.br/.
- Novos `scripts/checklist_submissao.py`, `scripts/carta_apresentacao.py`, `scripts/resposta_revisores.py` e `scripts/orcid_lattes_diff.py` (lê a API pública da ORCID e o XML exportado do Lattes; não altera registros).
- `sincronizar_manuais.py` sincroniza também o repositório `submissao-orcid-lattes-pesquisa-cientifica`.

## 1.0.13 — 2026-09-09
- Nova skill `ensino-pesquisa`: plano de ensino semana a semana ligado aos manuais, rubricas por entrega com o arquivo que prova, painel da turma, uso de IA na disciplina, estágio de docência, ligada ao manual https://professor.mirandastech.com.br/.
- Novos `scripts/plano_de_ensino.py`, `scripts/rubrica.py` e `scripts/turma_progresso.py`.
- `sincronizar_manuais.py` sincroniza também o repositório `manual-do-professor-pesquisa-cientifica`.

## 1.0.12 — 2026-09-09
- Nova skill `orientacao-academica`: acordo de orientação, atas de reunião com pendências, matriz CRediT e critérios ICMJE de autoria, relatório de progresso, integridade, ligada ao manual https://orientador.mirandastech.com.br/.
- Novos `scripts/acordo_orientacao.py`, `scripts/reuniao_orientacao.py` e `scripts/autoria_credit.py`.
- `sincronizar_manuais.py` sincroniza também o repositório `manual-do-orientador-pesquisa-cientifica`.

## 1.0.11 — 2026-09-09
- Nova skill `defesa-qualificacao`: regimento primeiro, roteiro da apresentação por bloco (Beamer compilado), ensaios cronometrados, banca simulada, checklist antes/no dia/depois, correções e versão final, ligada ao manual https://defesa.mirandastech.com.br/.
- Novos `scripts/apresentacao_defesa.py`, `scripts/ensaio_defesa.py` e `scripts/checklist_defesa.py`.
- `sincronizar_manuais.py` sincroniza também o repositório `defesa-qualificacao-pesquisa-cientifica`.

## 1.0.10 — 2026-09-09
- Nova skill `ciencia-aberta-preregistro`: pré-registro (OSF, AsPredicted, PROSPERO, ReBEC), plano de gestão de dados, depósito com DOI (Zenodo/OSF), preprints, licenças CC, FAIR, ORCID e Registered Reports, ligada ao manual https://cienciaaberta.mirandastech.com.br/.
- Novos `scripts/preregistro.py`, `scripts/deposito_zenodo.py` e `scripts/plano_gestao_dados.py`.
- `sincronizar_manuais.py` sincroniza também o repositório `ciencia-aberta-pesquisa-cientifica`.

## 1.0.9 — 2026-09-09
- Nova skill `bibliometria-vosviewer`: indicadores do corpus, redes de coautoria, termos, fontes e acoplamento bibliográfico nos formatos do VOSviewer e do VOSviewer Online, Bibliometrix como alternativa, relato responsável (Leiden, DORA), ligada ao manual https://bibliometria.mirandastech.com.br/.
- Novos `scripts/indicadores_bibliometricos.py` e `scripts/mapa_vosviewer.py`.
- `sincronizar_manuais.py` sincroniza também o repositório `bibliometria-pesquisa-cientifica`.

## 1.0.8 — 2026-09-09
- Nova skill `analise-de-dados`: limpeza documentada, descritivas, comparação entre grupos com tamanho de efeito e IC, correlação, tabela cruzada, figuras por script, codificação no Taguette e relato conforme SAMPL/COREQ, ligada ao manual https://dados.mirandastech.com.br/. O Pesquisador a chama na fase 7.
- Novos `scripts/limpar_dados.py` (relatório de limpeza sem apagar linhas), `scripts/analisar.py` (Welch t/Mann-Whitney, ANOVA/Kruskal, Pearson/Spearman, qui-quadrado/V de Cramér, boxplot) e `scripts/codificar_taguette.py` (etiqueta × documento, trechos, coocorrência).
- `sincronizar_manuais.py` sincroniza também o repositório `analise-de-dados-pesquisa-cientifica`.

## 1.0.7 — 2026-09-09
- Nova skill `git-github-pesquisadores`: controle de versão do projeto de pesquisa (o que entra e o que fica fora do Git, commits e tags por marco, README/LICENSE/CITATION.cff, release e DOI pelo Zenodo, auditoria antes de publicar), ligada ao manual https://git.mirandastech.com.br/. O Pesquisador a chama na fase 10.
- Novos `scripts/checar_repo.py` (auditoria: arquivos grandes, segredos, dados pessoais, README/LICENSE/CITATION.cff), `scripts/salvar_versao.sh` (commit + tag anotada) e `scripts/citacao_cff.py` (CITATION.cff 1.2.0 + BibTeX + ABNT).
- `sincronizar_manuais.py` sincroniza também o repositório `git-github-pesquisa-cientifica`.

## 1.0.6 — 2026-09-09
- Nova skill `latex-overleaf-abntex2`: trabalho acadêmico em LaTeX com o abnTeX2 no Overleaf ou local (TinyTeX), .bib do Zotero com Better BibTeX, latexmk e leitura do log, ligada ao manual https://latex.mirandastech.com.br/. O Pesquisador a chama na fase 8.
- Novos `scripts/compilar.sh`, `scripts/novo_trabalho.py` (projeto a partir do modelo canônico com os dados do aluno) e `scripts/checar_citacoes.py`.
- `sincronizar_manuais.py` sincroniza também o repositório `latex-overleaf-abntex2-pesquisa-cientifica`.

## 1.0.5 — 2026-09-09
- Nova skill `busca-bases-abertas`: estratégia por conceitos, sintaxe por base, diário PRISMA-S e buscas reprodutíveis por API, ligada ao manual https://busca.mirandastech.com.br/. O Pesquisador a chama na fase 4.
- Novos `scripts/buscar_openalex.py` (cursor, CSV + RIS + diário JSON), `scripts/contar_bases.py` (mesma pergunta em seis APIs) e `scripts/verificar_oa.py` (Unpaywall).
- `sincronizar_manuais.py` sincroniza também o repositório `busca-bases-pesquisa-cientifica`.

## 1.0.4 — 2026-09-09
- Nova skill `revisao-sistematica-prisma`: revisão sistemática do protocolo ao relato com PRISMA 2020 (registro no PROSPERO/OSF, busca reprodutível, deduplicação, triagem no ASReview LAB ou Rayyan, dupla triagem com kappa, extração, qualidade, fluxograma e checklist), ligada ao manual https://prisma.mirandastech.com.br/. O Pesquisador a chama nas fases 4, 5 e 8.
- Novos `scripts/deduplicar.py` (DOI e título normalizado, com arquivo de auditoria) e `scripts/kappa.py` (tabela 2×2, po, pe, κ e faixa de Landis e Koch).
- Novos modelos `BUSCA.md` (diário de busca PRISMA-S), `CODEBOOK.md` e `CONTAGENS.md` (uma linha por caixa do fluxograma); `iniciar_projeto.py` os copia para `01_buscas/` e `02_triagem/`.
- `sincronizar_manuais.py` passa a sincronizar também o repositório `revisao-sistematica-pesquisa-cientifica`.

## 1.0.3 — 2026-09-09
- Suíte de testes dos agentes em `evals/` (`claude plugin eval`): nove casos com projeto preparado por cenário (`_lib/projeto.sh`), graders regex, tool_used, file_exists e juiz LLM; primeira rodada 8/8 nos casos de conversa. Ver `evals/README.md`.
- `PROGRESSO.md` declara a versão do esquema (`<!-- esquema: 1 -->`); `iniciar_projeto.py` avisa quando o arquivo é de esquema mais antigo ou mais novo que o plugin.
- Skill do Pesquisador ganha a seção «Sem pasta de projeto (ChatGPT no navegador)»: estrutura em .zip, anexos com caminho, `PROGRESSO.md` colado a cada conversa, nada inventado.
- `scripts/sincronizar_manuais.py`: o plugin passa a ser a fonte única dos agentes, skills, scripts e modelos compartilhados com os repositórios dos quatro manuais (`--verificar` no CI, `--aplicar` para reescrever).
- `exemplos/`: dois projetos fictícios preenchidos (revisão na fase 6; estudo de caso na fase 8), regeneráveis por `exemplos/gerar_exemplos.py`.
- Capturas e PDF do manual saem do Git para a release `manual-assets`; o Dockerfile do manual e o do hub baixam o zip no build (clone do plugin ~5 MB mais leve).
- Corrigida uma frase truncada no agente Bibliotecário.

## 1.0.2 — 2026-09-09
- `scripts/relatorio_orientador.py`: relatório para o orientador gerado só dos arquivos do projeto (fases, checklists com evidência, decisões datadas, uso de IA por etapa); `/pesquisa:status` passa a gerá-lo em `00_projeto/RELATORIO_ORIENTADOR.md` antes de comentar.
- Hook de início de sessão usa `scripts/resumo_sessao.py`: fase atual, fases fechadas, contagem dos checklists, última decisão datada, usos de IA e há quantos dias o `PROGRESSO.md` não muda.
- Descrições das sete ferramentas do conector Zotero trazem os nomes dos parâmetros e exemplos de chamada.

## 1.0.1 — 2026-09-09
- Modelos `USO_DE_IA.csv` e `registro_exportacoes.csv` nascem só com o cabeçalho; as linhas de exemplo foram para `modelos/exemplos/` (os agentes liam o exemplo como dado do projeto). `DECISOES.md` avisa que D001 e D002 são esqueletos.
- Novo `scripts/registrar_desktop.py` (`--verificar` / `--registrar`, com backup): registra o conector Zotero no Claude Desktop; o `/pesquisa:iniciar` oferece isso ao aluno e o `instalar_claude.sh` passa a usá-lo.
- `instalar_codex.sh` pergunta (ou `--auto`) e escreve `approval_mode = "auto"` para as sete ferramentas do conector, com backup do `config.toml`.
- Manual do plugin publicado em https://plugin.mirandastech.com.br/ (pasta `manual/`).

## 1.0.0 — 2026-09-08
- Primeira versão: Pesquisador, Metodólogo, Orientador, Bibliotecário; 9 skills; 7 comandos; conector Zotero; hook; pacote do Codex publicado no diretório do ChatGPT/Codex.
