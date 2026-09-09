# Histórico de versões

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
