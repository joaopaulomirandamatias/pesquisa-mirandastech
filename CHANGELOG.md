# Histórico de versões

## 1.0.1 — 2026-09-09
- Modelos `USO_DE_IA.csv` e `registro_exportacoes.csv` nascem só com o cabeçalho; as linhas de exemplo foram para `modelos/exemplos/` (os agentes liam o exemplo como dado do projeto). `DECISOES.md` avisa que D001 e D002 são esqueletos.
- Novo `scripts/registrar_desktop.py` (`--verificar` / `--registrar`, com backup): registra o conector Zotero no Claude Desktop; o `/pesquisa:iniciar` oferece isso ao aluno e o `instalar_claude.sh` passa a usá-lo.
- `instalar_codex.sh` pergunta (ou `--auto`) e escreve `approval_mode = "auto"` para as sete ferramentas do conector, com backup do `config.toml`.
- Manual do plugin publicado em https://plugin.mirandastech.com.br/ (pasta `manual/`).

## 1.0.0 — 2026-09-08
- Primeira versão: Pesquisador, Metodólogo, Orientador, Bibliotecário; 9 skills; 7 comandos; conector Zotero; hook; pacote do Codex publicado no diretório do ChatGPT/Codex.
