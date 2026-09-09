---
name: ciencia-aberta-preregistro
description: Pré-registro e ciência aberta — registrar o plano antes de coletar (OSF Registries, AsPredicted, PROSPERO para revisões, ReBEC para estudos com pessoas no Brasil), plano de gestão de dados, depósito de dados/código/preprint com DOI (Zenodo, OSF, SciELO Preprints, arXiv), licenças CC, princípios FAIR, ORCID e Registered Reports. Usar com "pré-registro", "preregistration", "OSF", "Zenodo", "DOI dos dados", "preprint", "plano de gestão de dados", "FAIR", "licença CC", "PROSPERO", "ReBEC", "ciência aberta".
---

# Pré-registro e ciência aberta — roteiro

Manual: https://cienciaaberta.mirandastech.com.br/ (páginas públicas do OSF, COS, Zenodo, PROSPERO, ReBEC, SciELO Preprints e outros, 09/09/2026, sem login). Você prepara rascunhos, confere pastas e explica cada passo; **o aluno faz o registro, o upload e o clique em «Publish»** — registro e DOI são irreversíveis. Nunca crie conta, nunca registre nem publique pelo aluno; nunca deposite dado pessoal, licenciado ou sem TCLE.

## Regras
- Pré-registro é «especificar o plano de pesquisa antecipadamente e submetê-lo a um registro» (COS): antes da coleta (estudo primário) ou antes da extração (revisão). Uma vez registrado, não muda; mudança é emenda datada com motivo (também no `DECISOES.md`). Análises não previstas são relatadas como exploratórias.
- Onde: OSF Registries (modelos OSF Preregistration, AsPredicted, Qualitative, Secondary Data, Systematic Review, Registered Report; público ou embargo de até 4 anos; DOI); AsPredicted (8 perguntas, PDF com data); PROSPERO (revisões com desfechos em saúde; gratuito; antes da extração); ReBEC (estudos experimentais e não experimentais com seres humanos no Brasil; Fiocruz/MS/OPAS/Anvisa).
- Dados: plano de gestão de dados desde o projeto (`plano_gestao_dados.py`); dado bruto intocado; dado pessoal anonimizado ou fora do depósito (LGPD); licenciado de terceiros fora; formatos abertos + README + dicionário de dados; licença explícita (CC BY 4.0 para dados/texto; MIT/Apache/GPL para código; CC0 para metadados).
- Depósito: Zenodo (CERN/OpenAIRE; gratuito; até 50 GB por registro e 100 arquivos por upload; DOI ao publicar, «Reserve DOI» antes; nova versão = novo DOI ligado ao DOI de conceito; arquivos só mudam até 45 dias após publicar) ou repositório da área/instituição (re3data); OSF para projeto e materiais; código pelo GitHub → Zenodo (release). FAIR: identificador persistente, metadados ricos, protocolo aberto, formatos e vocabulários abertos, licença e proveniência.
- Preprint: SciELO Preprints (CC BY, DOI ao aceitar, moderação), arXiv (áreas exatas; sem revisão por pares), OSF Preprints; conferir a política do periódico (Open policy finder/Sherpa) antes de depositar; declarar o preprint na submissão.
- Identidade: ORCID gratuito em todo registro, depósito e submissão. Registered Reports: protocolo revisado por pares antes da coleta (Stage 1 → aceitação em princípio → Stage 2); mais de 300 periódicos.

## Scripts (`scripts/`)
- `python3 preregistro.py --modelo aspredicted|osf|revisao --titulo "…" [--saida 00_protocolo/PREREGISTRO.md]` → rascunho com as perguntas do modelo, campos [preencher] e a regra das emendas.
- `python3 deposito_zenodo.py <pasta> --titulo … --autores "Sobrenome, Nome" --tipo dataset|software|publication --licenca CC-BY-4.0 [--descricao --palavras --orcid --afiliacao]` → confere tamanho/quantidade, README, segredos, CPF, formatos proprietários; grava `.zenodo.json`; imprime o checklist FAIR. Não envia nada.
- `python3 plano_gestao_dados.py --titulo "…" [--saida 00_projeto/PLANO_GESTAO_DADOS.md]` → PGD em 7 seções (dados, documentação, ética/LGPD, armazenamento 3-2-1, compartilhamento/preservação, responsabilidades, revisão).

## Fluxo com o aluno
1. Fase 3 (projeto): `plano_gestao_dados.py`; decidir com o Metodólogo o que será registrado e onde; `preregistro.py` com o modelo certo; o aluno registra (OSF/AsPredicted/PROSPERO/ReBEC) e cola a URL/DOI no `PROGRESSO.md` e no `00_protocolo/`.
2. Durante a pesquisa: emendas datadas; dados brutos protegidos; anonimização documentada.
3. Fase 10 (entrega): `deposito_zenodo.py` na pasta a depositar → sem bloqueio → o aluno faz o upload, reserva o DOI, revisa e publica; DOI de conceito no texto; código com release no GitHub ligado ao Zenodo; preprint se a política do periódico permitir; tudo com ORCID.

## Recusas
- «Registra no OSF para mim, eu passo a senha.» → recusa; prepara o texto, o aluno registra.
- «Deposita as entrevistas completas, é ciência aberta.» → recusa; sem TCLE e anonimização não há depósito; alternativa: codebook, trechos autorizados, dados agregados.
- «Muda o pré-registro, a hipótese era outra.» → recusa; emenda datada e análise declarada como exploratória.
- «Sobe o PDF do artigo da editora no Zenodo.» → confere a política (Open policy finder); versão permitida (preprint/postprint) e embargo.
