#!/usr/bin/env bash
# Instala o plugin Pesquisa MirandasTech no Claude Code (marketplace + plugin) e o conector Zotero no Claude Desktop, se existir.
# Alternativa manual no Claude Code:  /plugin marketplace add joaopaulomirandamatias/pesquisa-mirandastech  →  /plugin install pesquisa@mirandastech
set -e
AQUI="$(cd "$(dirname "$0")/.." && pwd)"; SRV="$AQUI/scripts/zotero_mcp.py"
if command -v claude >/dev/null; then
  claude plugin marketplace add joaopaulomirandamatias/pesquisa-mirandastech 2>/dev/null || claude plugin marketplace update mirandastech || true
  claude plugin install pesquisa@mirandastech && echo "Claude Code: plugin pesquisa instalado (agentes, skills, comandos /pesquisa, conector zotero)"
else
  echo "Claude Code não encontrado; instale-o e rode: /plugin marketplace add joaopaulomirandamatias/pesquisa-mirandastech"
fi
command -v uv >/dev/null || echo "Aviso: o conector Zotero usa uv (https://docs.astral.sh/uv/); sem ele, troque o comando por python3 com 'pip install mcp'."
for CFG in "$HOME/.config/Claude/claude_desktop_config.json" "$HOME/Library/Application Support/Claude/claude_desktop_config.json" "$APPDATA/Claude/claude_desktop_config.json"; do
  [ -f "$CFG" ] || continue
  python3 - "$CFG" "$SRV" <<'PY'
import json,sys; p,srv=sys.argv[1],sys.argv[2]; d=json.load(open(p))
d.setdefault("mcpServers",{})["zotero"]={"command":"uv","args":["run","--with","mcp","python",srv]}
json.dump(d,open(p,"w"),indent=2,ensure_ascii=False); print("Claude Desktop: conector zotero adicionado em",p,"(reinicie o app)")
PY
done
echo; echo 'Na pasta do projeto, no Claude Code: "Pesquisador, começar minha pesquisa" ou /pesquisa:iniciar'
