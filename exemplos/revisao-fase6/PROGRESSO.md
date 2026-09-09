# Progresso — Manutenção preditiva com IA em terminais portuários
<!-- esquema: 1 · gerado por iniciar_projeto.py do plugin Pesquisa MirandasTech -->
> **Exemplo fictício** gerado por `exemplos/gerar_exemplos.py`: estudos, números e pessoas são inventados; serve para mostrar o formato preenchido.

**Método provável:** revisão sistemática · **Programa:** PPGEE · **Prazo:** 2027-03 · **Início:** 2026-09-08
Manuais: https://metodologia.mirandastech.com.br/ · https://manual.mirandastech.com.br/ · https://zotero.mirandastech.com.br/ · https://notebook.mirandastech.com.br/

Regra: um item só é marcado `[x]` pelo agente responsável depois de conferir a evidência (arquivo, script, número). Anote data e evidência ao lado. O aluno decide; o agente formula e registra em DECISOES.md.

## Fases (Pesquisador)

| Fase | Nome | Porta de saída | Quem conduz | Estado | Data | Evidência |
|---|---|---|---|---|---|---|
| 0 | Diagnóstico | Tema, prazo, programa, orientador e ferramentas registrados; pasta criada | Pesquisador | [x] | 2026-03-10 | cabeçalho; ACORDO_ORIENTADOR.md assinado |
| 1 | Pergunta | Tema delimitado → problema → pergunta com tabela vazia do resultado → objetivos | Metodólogo | [x] | 2026-03-24 | 00_projeto/DECISOES_METODO.md §1–3 |
| 2 | Método | Classificação, desenho, amostra, instrumento, análise; o que a IA pode fazer aqui | Metodólogo · Orientador | [x] | 2026-04-07 | DECISOES_METODO.md §4–8; D003 |
| 3 | Projeto e ética | Projeto NBR 15287:2025; parecer do CEP quando houver pessoas | Metodólogo | [x] | 2026-04-28 | 06_texto/projeto_nbr15287.md; sem pessoas → CEP não se aplica (D004) |
| 4 | Busca e biblioteca | Bases, strings verbatim, coleção por base e data; auditoria da biblioteca | Metodólogo · Bibliotecário | [x] | 2026-05-19 | 01_buscas/buscas.csv (3 bases); registro_exportacoes.csv com SHA-256; auditoria sem pendências críticas |
| 5 | Triagem | Deduplicação, triagem assistida com status preliminar, decisão do aluno, números do PRISMA | Orientador · Bibliotecário | [x] | 2026-06-30 | 02_triagem/prisma.md: 412 → 287 → 41 → 18 incluídos; κ = 0,81 (IC 0,72–0,90) |
| 6 | Leitura e síntese | PDFs do Zotero → notebook; fichamento; matriz de síntese conferida célula a célula | Leitura (Gemini Notebook) | [ ] | | |
| 7 | Análise | Coleta e análise conforme o método; IA só onde autorizada e registrada | Metodólogo · Orientador | [ ] | | |
| 8 | Escrita ABNT | NBR 14724, 10520, 6023 via Zotero; verificação automática de citações e referências | Bibliotecário · scripts | [ ] | | |
| 9 | Pré-banca | Cinco objeções mais fortes, perguntas prováveis, respostas com página | Metodólogo · Leitura | [ ] | | |
| 10 | Entrega | Declaração de uso de IA, backup, versão congelada da biblioteca, checklist final | Orientador · Bibliotecário | [ ] | | |

## Método (Metodólogo) — slides em metodologia.mirandastech.com.br

| # | Área | Item | Slides | Estado | Data | Evidência conferida |
|---|---|---|---|---|---|---|
| M1 | Pergunta | Pergunta clara, delimitada, empírica e viável; tabela vazia do resultado | 7 | [x] | 2026-03-24 | DECISOES_METODO.md §1 |
| M2 | Objetivos | Objetivo geral = pergunta em ação; específicos geram resultado, não etapa | 8 | [x] | 2026-03-24 | §2 |
| M3 | Justificativa | Lacuna apontada com revisões; relevância; contribuição verificável | 9 | [x] | 2026-03-24 | §3 (duas revisões: Chen 2022; Okoro 2023) |
| M4 | Revisão | Buscas registradas; matriz de síntese; fichas com página | 10–11 | [x] | 2026-06-30 | 01_buscas/; 04_sintese/matriz_sintese.csv em preenchimento |
| M5 | Classificação | Natureza, abordagem, objetivo e procedimento — uma resposta por eixo | 12 | [x] | 2026-04-07 | §4 |
| M6 | Método | Frase «escolhi X porque…; descartei Y porque…» registrada | 14 | [x] | 2026-04-07 | §5 |
| M7 | Amostra | População, unidade, amostragem, n calculado e obtido | 16 | [x] | 2026-04-07 | §7 elegibilidade |
| M8 | Instrumento | Tabela de operacionalização; juízes; pré-teste registrado | 18 | [x] | 2026-04-07 | §8 formulário de extração |
| M9 | Ética | Parecer do CEP com CAAE antes da coleta; TCLE arquivado; LGPD | 6, 27 | [x] | 2026-04-28 | D004: sem participantes humanos |
| M10 | Análise | Técnica decidida antes; pressupostos; efeito com IC; categorias com trecho | 21–22 | [ ] | | |
| M11 | Reprodutibilidade | Dados, scripts, ambiente e decisões guardados; figura por script | 24 | [ ] | | |
| M12 | Estrutura | NBR 14724:2024 / 15287:2025 e modelo do programa | 25, 28 | [x] | 2026-04-28 | 06_texto/projeto_nbr15287.md |
| M13 | Citações | NBR 10520:2023; diretas com página; sem paráfrase próxima | 30 | [ ] | | |
| M14 | Referências | NBR 6023:2025 via gerenciador; DOI resolvido; texto ↔ lista | 31 | [ ] | | |
| M15 | Texto | Números batem com tabelas; conclusão por objetivo; limites explícitos | 32 | [ ] | | |
| M16 | Defesa | Cinco objeções com resposta; ensaio; material à mão | 34 | [ ] | | |

## Uso de IA (Orientador) — slides em manual.mirandastech.com.br

| # | Área | Item | Slides | Estado | Data | Evidência conferida |
|---|---|---|---|---|---|---|
| I1 | Governança | Acordo com o orientador assinado; protocolo congelado e datado antes da primeira busca; procedimento de emenda escrito | 6, 17 | [x] | 2026-04-14 | ACORDO_ORIENTADOR.md; 00_protocolo/protocolo.md congelado em 2026-04-14 |
| I2 | Governança | Arquivo de regras do agente com proibições absolutas, gates humanos e critério de conclusão | 37 | [x] | 2026-03-10 | AGENTS.md |
| I3 | Dados | Dado licenciado e pessoal fora do repositório; treinamento desligado nas ferramentas; hash registrado | 9, 11 | [x] | 2026-05-19 | dados_FORA_DO_GIT/; hashes em registro_exportacoes.csv |
| I4 | Busca | String de cada base salva verbatim do histórico, com data, filtros, total e SHA-256 do export | 18, 22 | [x] | 2026-05-19 | 01_buscas/buscas.csv |
| I5 | Busca | Teste com e sem truncamento registrado; conjunto-semente com regra de decisão prévia | 19, 21 | [x] | 2026-05-12 | 01_buscas/teste_truncamento.md |
| I6 | Triagem | Codebook versionado; toda recomendação de IA com status preliminar; decisão humana por registro | 23, 28 | [x] | 2026-06-02 | 05_analise/livro_de_codigos.csv v2; USO_DE_IA.csv linhas 1–3 |
| I7 | Triagem | κ com intervalo de confiança; grau de cegamento declarado; regra de parada do aprendizado ativo escrita antes | 26, 27 | [x] | 2026-06-30 | 02_triagem/kappa.md |
| I8 | Acesso | Os três números do texto completo medidos separadamente; E5 declarado com lista | 31 | [x] | 2026-07-14 | 02_triagem/texto_completo.md: 41 elegíveis, 39 obtidos, 2 E5 |
| I9 | Extração | Cada codificação com página e seção; extração assistida conferida no PDF; dupla codificação em amostra | 32, 33 | [ ] | | |
| I10 | Figuras | Toda figura gerada por script que lê o dado; nenhum número digitado; nenhuma imagem gerada por IA | 34 | [ ] | | |
| I11 | Referências | Todo DOI resolvido na Crossref na versão final; referência sem DOI com prova alternativa | 42 | [ ] | | |
| I12 | Texto | Marcas de IA contadas e removidas; um trecho lido em voz alta; comparação linha a linha com a versão do modelo | 40, 41 | [ ] | | |
| I13 | Texto | Todo número do texto bate com a tabela de origem; somas fecham; resumo contado | 44 | [ ] | | |
| I14 | Equipe | Registro de uso compartilhado com a coluna «quem»; todos os coautores leram o texto inteiro e aprovaram a declaração | 12, 13 | [ ] | | |
| I15 | Declaração | Uso de IA declarado com ferramenta, fase, finalidade, validação e o que a IA não fez | 43 | [ ] | | |
| I16 | Entrega | Guia de relato conferido item a item; disponibilidade de dados verdadeira no momento da submissão | 16 | [ ] | | |

## Biblioteca (Bibliotecário) — slides em zotero.mirandastech.com.br

| # | Área | Item | Slides | Estado | Data | Evidência conferida |
|---|---|---|---|---|---|---|
| B1 | Instalação | Zotero instalado do site oficial; Connector no navegador; ícone testado numa página com DOI | 6–9 | [x] | 2026-03-17 | item de teste 10.1016/j.jii.2023.100xxx importado |
| B2 | Conta | Sincronização automática ligada; decisão sobre arquivos (Storage/WebDAV/nenhum) registrada | 10 | [x] | 2026-03-17 | D005: sincronização + Storage |
| B3 | Configurações | Idioma pt-BR; PDF automático e acesso aberto; renomeação automática; pasta de dados fora de nuvem sincronizada | 11 | [x] | 2026-03-17 | pasta de dados em ~/Zotero |
| B4 | Estilo | Estilo ABNT instalado e testado com artigo, livro e tese; idioma da citação pt-BR | 30–31 | [x] | 2026-03-17 | ABNT testado com 3 tipos |
| B5 | Editor | Aba/menu Zotero visível no editor; Preferências do documento com ABNT | 32–33 | [ ] | | |
| B6 | Estrutura | Coleções por etapa e convenção de etiquetas escritas em DECISOES.md | 20–21 | [x] | 2026-04-07 | tools/zotero_estrutura_colecoes.md |
| B7 | Auditorias | Pesquisas salvas «sem DOI», «sem PDF», «página da web» criadas | 22 | [x] | 2026-04-07 | pesquisas salvas criadas |
| B8 | Auditoria | scripts/auditar_biblioteca.py sem pendências críticas | 49 | [x] | 2026-05-19 | auditoria.csv sem críticas |
| B9 | Leitura | Convenção de cores das anotações definida; nota extraída com página testada | 27–28 | [ ] | | |
| B10 | Exportação | Better BibTeX se houver LaTeX/Obsidian; .bib com «Manter atualizado» | 38 | [ ] | | |
| B11 | Backup | Backup da pasta de dados feito com o Zotero fechado; rotina agendada | 41 | [ ] | | |
| B12 | Grupo | Se há coautores: grupo privado criado, permissões e dono definidos | 44 | [ ] | | |

## Leitura e síntese (Gemini Notebook) — slides em notebook.mirandastech.com.br

| # | Área | Item | Slides | Estado | Data | Evidência conferida |
|---|---|---|---|---|---|---|
| L1 | Conta | Conta pessoal ou institucional escolhida sabendo a diferença de privacidade | 7, 43 | [x] | 2026-07-14 | conta institucional (D006) |
| L2 | Fontes | PDFs nomeados «Autor - Ano - Título» (do Zotero); nenhuma URL de editora; nenhum PDF escaneado sem OCR | 11–14 | [x] | 2026-07-14 | 18 PDFs «Autor - Ano - Título» do Zotero |
| L3 | Ingestão | Pergunta de inventário rodada; guia de cada fonte aberto; fontes vazias corrigidas | 19 | [x] | 2026-07-21 | tools/inventario_notebook.md |
| L4 | Citações | Trecho aberto e lido para cada afirmação usada; frases sem número descartadas | 21 | [ ] | | |
| L5 | Matriz | Colunas definidas pelo protocolo; primeira versão pelo notebook; cada célula conferida na planilha | 34 | [ ] | | |
| L6 | Dados sensíveis | Nada identificável enviado; transcrições anonimizadas; feedback não enviado em conversas com dados | 43–45 | [ ] | | |
| L7 | Declaração | Uso do notebook na leitura declarado; nada do Estúdio citado no texto | 45 | [ ] | | |
