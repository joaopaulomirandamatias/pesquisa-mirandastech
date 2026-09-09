#!/usr/bin/env bash
# Instala o plugin no Codex (marketplace próprio), registra o conector MCP «zotero», instala os prompts
# /pesquisador /metodologo /orientador /bibliotecario e, com o seu consentimento, libera as sete ferramentas
# do conector (todas só leem a biblioteca) para rodarem sem pedir aprovação a cada chamada.
#   bash scripts/instalar_codex.sh          # pergunta antes de escrever o approval_mode
#   bash scripts/instalar_codex.sh --auto   # não pergunta (uso em scripts)
set -e
AQUI="$(cd "$(dirname "$0")/.." && pwd)"; SRV="$AQUI/scripts/zotero_mcp.py"; CFG="$HOME/.codex/config.toml"
FERRAMENTAS="status listar_colecoes buscar_itens detalhar_item referencia_abnt auditar exportar_bbt"
if command -v codex >/dev/null; then
  codex plugin marketplace add joaopaulomirandamatias/pesquisa-mirandastech >/dev/null 2>&1 || codex plugin marketplace upgrade mirandastech >/dev/null 2>&1 || true
  codex plugin add pesquisa-mirandastech@mirandastech >/dev/null 2>&1 && echo "Codex: plugin pesquisa-mirandastech instalado (skills e AGENTS.md)" || true
  codex mcp remove zotero >/dev/null 2>&1 || true
  codex mcp add zotero -- uv run --with mcp python "$SRV" && echo "Codex: conector zotero registrado em $CFG"
else
  mkdir -p ~/.codex; printf '\n[mcp_servers.zotero]\ncommand = "uv"\nargs = ["run", "--with", "mcp", "python", "%s"]\n' "$SRV" >> "$CFG"; echo "Codex: seção [mcp_servers.zotero] acrescentada em $CFG"
fi
mkdir -p ~/.codex/prompts && cp "$AQUI"/codex/prompts/*.md ~/.codex/prompts/ && echo "Codex: prompts /pesquisador /metodologo /orientador /bibliotecario instalados"

# approval_mode = "auto" por ferramenta (só leitura): pergunta, salvo --auto
RESP="n"
if [ "${1:-}" = "--auto" ]; then RESP="s"
elif [ -t 0 ]; then
  echo; echo "O Codex pede aprovação a cada chamada de ferramenta MCP. As sete ferramentas do conector zotero só leem a biblioteca"
  echo "(status, listar_colecoes, buscar_itens, detalhar_item, referencia_abnt, auditar, exportar_bbt)."
  read -r -p "Liberar as sete para rodar sem aprovação (approval_mode = \"auto\" em $CFG)? [s/N] " RESP
fi
if [ "$RESP" = "s" ] || [ "$RESP" = "S" ]; then
  cp "$CFG" "$CFG.bak-pesquisa"; N=0
  for T in $FERRAMENTAS; do
    grep -q "^\[mcp_servers.zotero.tools.$T\]" "$CFG" 2>/dev/null && continue
    printf '\n[mcp_servers.zotero.tools.%s]\napproval_mode = "auto"\n' "$T" >> "$CFG"; N=$((N+1))
  done
  echo "Codex: approval_mode = \"auto\" escrito para $N ferramenta(s) (backup em $CFG.bak-pesquisa)"
else
  echo "Codex: approval_mode não alterado. Para liberar depois, rode este script de novo ou acrescente por ferramenta em $CFG:"
  echo '  [mcp_servers.zotero.tools.auditar]'; echo '  approval_mode = "auto"'
fi
echo; echo "Abra o Codex na pasta do projeto (ele lê AGENTS.md) e peça: /pesquisador onde paramos"
