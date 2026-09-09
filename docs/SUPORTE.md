# Suporte — Pesquisa MirandasTech

- **Dúvidas sobre o plugin, instalação e agentes:** abra uma issue em https://github.com/joaopaulomirandamatias/pesquisa-mirandastech/issues (em português ou inglês). Diga o cliente (Claude Code, Claude Desktop, Codex app ou CLI), o sistema operacional e o que aconteceu.
- **E-mail:** contato@mirandastech.com.br.
- **Hub de pesquisa e manuais:** https://www.mirandastech.com.br/pesquisa — Metodologia (https://metodologia.mirandastech.com.br/), Uso de IA (https://manual.mirandastech.com.br/), Zotero (https://zotero.mirandastech.com.br/), Gemini Notebook (https://notebook.mirandastech.com.br/).
- **Antes de abrir uma issue:** rode `claude plugin validate` (Claude Code) ou `codex plugin list` (Codex) e, para o conector Zotero, confirme que o Zotero está aberto com a API local ligada (Configurações → Avançado → «Permitir que outros aplicativos neste computador se comuniquem com o Zotero») e que `uv` está instalado.
- **Política de privacidade:** docs/PRIVACIDADE.md · **Termos de uso:** docs/TERMOS.md.

## Problemas conhecidos
| Sintoma | Causa | Solução |
|---|---|---|
| O conector `zotero` aparece desconectado | Zotero fechado, API local desligada ou `uv` ausente | Abra o Zotero, ligue a API local; instale o `uv` ou troque o comando do conector por `python3` com `pip install mcp` |
| No Codex, cada chamada ao conector pede aprovação | Política padrão do Codex para ferramentas MCP | Rode `bash scripts/instalar_codex.sh` e responda «s» quando ele perguntar; ou, em `~/.codex/config.toml`, por ferramenta: `[mcp_servers.zotero.tools.auditar]` `approval_mode = "auto"` (todas só leem) |
| O Claude Desktop não mostra o conector `zotero` | A instalação pelo marketplace só configura o Claude Code | `python3 scripts/registrar_desktop.py --registrar` (ou aceite a oferta do `/pesquisa:iniciar`) e reinicie o app |
| O Pesquisador pergunta sobre uma linha de março de 2026 no `USO_DE_IA.csv` | Projeto criado com a versão 1.0.0, cujos modelos traziam uma linha de exemplo | Apague a linha; desde a 1.0.1 os modelos nascem vazios e os exemplos ficam em `modelos/exemplos/` |
| `verificar_refs.py` sem rede | O script consulta a Crossref | Rode com internet; sem rede ele só valida o formato |
| `PROGRESSO_IA.md` e `PROGRESSO_METODOLOGIA.md` antigos na pasta | Projeto criado pelos manuais anteriores | `iniciar_projeto.py` migra os itens marcados para `PROGRESSO.md` e mantém os antigos como histórico |
