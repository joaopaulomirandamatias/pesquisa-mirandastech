# Histórico de versões

## Não publicado
- Suíte de testes dos agentes em `evals/` (`claude plugin eval`): oito casos com projeto preparado por cenário (`_lib/projeto.sh`), graders regex, tool_used e juiz LLM. Ver `evals/README.md`.

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
