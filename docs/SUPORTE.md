# Suporte — Pesquisa MirandasTech

- **Dúvidas sobre o plugin, instalação e agentes:** abra uma issue em https://github.com/joaopaulomirandamatias/pesquisa-mirandastech/issues (em português ou inglês). Diga o cliente (Claude Code, Claude Desktop, Codex app ou CLI), o sistema operacional e o que aconteceu.
- **E-mail:** joaopaulomirandamatias@gmail.com.
- **Hub de pesquisa e manuais:** https://www.mirandastech.com.br/pesquisa — Metodologia (https://metodologia.mirandastech.com.br/), Uso de IA (https://manual.mirandastech.com.br/), Zotero (https://zotero.mirandastech.com.br/), Gemini Notebook (https://notebook.mirandastech.com.br/).
- **Antes de abrir uma issue:** rode `claude plugin validate` (Claude Code) ou `codex plugin list` (Codex) e, para o conector Zotero, confirme que o Zotero está aberto com a API local ligada (Configurações → Avançado → «Permitir que outros aplicativos neste computador se comuniquem com o Zotero») e que `uv` está instalado.
- **Política de privacidade:** docs/PRIVACIDADE.md · **Termos de uso:** docs/TERMOS.md.

## Problemas conhecidos
| Sintoma | Causa | Solução |
|---|---|---|
| O conector `zotero` aparece desconectado | Zotero fechado, API local desligada ou `uv` ausente | Abra o Zotero, ligue a API local; instale o `uv` ou troque o comando do conector por `python3` com `pip install mcp` |
| No Codex, cada chamada ao conector pede aprovação | Política padrão do Codex para ferramentas MCP | Em `~/.codex/config.toml`, por ferramenta: `[mcp_servers.zotero.tools.auditar]` `approval_mode = "auto"` (todas só leem) |
| `verificar_refs.py` sem rede | O script consulta a Crossref | Rode com internet; sem rede ele só valida o formato |
| `PROGRESSO_IA.md` e `PROGRESSO_METODOLOGIA.md` antigos na pasta | Projeto criado pelos manuais anteriores | `iniciar_projeto.py` migra os itens marcados para `PROGRESSO.md` e mantém os antigos como histórico |
