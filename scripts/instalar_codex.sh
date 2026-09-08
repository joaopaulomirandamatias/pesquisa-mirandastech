#!/usr/bin/env bash
# Registra o conector MCP «zotero» no Codex (CLI e app) e instala os prompts /pesquisador, /metodologo, /orientador, /bibliotecario.
set -e
AQUI="$(cd "$(dirname "$0")/.." && pwd)"; SRV="$AQUI/scripts/zotero_mcp.py"
if command -v codex >/dev/null; then
  codex plugin marketplace add joaopaulomirandamatias/pesquisa-mirandastech >/dev/null 2>&1 || codex plugin marketplace upgrade mirandastech >/dev/null 2>&1 || true
  codex plugin add pesquisa-mirandastech@mirandastech >/dev/null 2>&1 && echo "Codex: plugin pesquisa-mirandastech instalado (skills e AGENTS.md)" || true
  codex mcp remove zotero >/dev/null 2>&1 || true
  codex mcp add zotero -- uv run --with mcp python "$SRV" && echo "Codex: conector zotero registrado em ~/.codex/config.toml"
else
  mkdir -p ~/.codex; printf '\n[mcp_servers.zotero]\ncommand = "uv"\nargs = ["run", "--with", "mcp", "python", "%s"]\n' "$SRV" >> ~/.codex/config.toml; echo "Codex: seção [mcp_servers.zotero] acrescentada em ~/.codex/config.toml"
fi
mkdir -p ~/.codex/prompts && cp "$AQUI"/codex/prompts/*.md ~/.codex/prompts/ && echo "Codex: prompts /pesquisador /metodologo /orientador /bibliotecario instalados"
echo "Dica: para as ferramentas do conector rodarem sem aprovação a cada chamada (todas só leem), acrescente por ferramenta em ~/.codex/config.toml:"; echo '  [mcp_servers.zotero.tools.auditar]'; echo '  approval_mode = "auto"'
echo; echo "Abra o Codex na pasta do projeto (ele lê AGENTS.md) e peça: /pesquisador onde paramos"
