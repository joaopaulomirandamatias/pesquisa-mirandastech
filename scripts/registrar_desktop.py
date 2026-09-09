#!/usr/bin/env python3
"""Registra o conector «zotero» no Claude Desktop (claude_desktop_config.json).

  python3 registrar_desktop.py --verificar   # só informa: arquivo encontrado? conector presente?
  python3 registrar_desktop.py --registrar   # escreve a entrada (faz backup .bak-pesquisa) e pede reinício do app

Nunca escreve sem --registrar. Usado pelo comando /pesquisa:iniciar depois do consentimento do aluno e pelo instalar_claude.sh."""
import json, os, shutil, sys
from pathlib import Path

SRV = Path(__file__).resolve().with_name("zotero_mcp.py")
CANDIDATOS = [Path.home() / ".config/Claude/claude_desktop_config.json",
              Path.home() / "Library/Application Support/Claude/claude_desktop_config.json",
              Path(os.environ.get("APPDATA", "")) / "Claude/claude_desktop_config.json" if os.environ.get("APPDATA") else None]
ENTRADA = {"command": "uv", "args": ["run", "--with", "mcp", "python", str(SRV)]}

def localizar():
    for p in CANDIDATOS:
        if p and p.is_file(): return p
    return None

def main(argv):
    modo = argv[1] if len(argv) > 1 else "--verificar"
    cfg = localizar()
    if not cfg:
        print("Claude Desktop: arquivo de configuração não encontrado (o app não está instalado ou nunca abriu Configurações → Desenvolvedor)."); return 2
    try: d = json.loads(cfg.read_text(encoding="utf-8") or "{}")
    except json.JSONDecodeError as e:
        print(f"Claude Desktop: {cfg} não é JSON válido ({e}); corrija antes de registrar."); return 3
    atual = d.get("mcpServers", {}).get("zotero")
    if modo == "--verificar":
        if atual == ENTRADA: print(f"Claude Desktop: conector zotero já registrado em {cfg}.")
        elif atual: print(f"Claude Desktop: há um conector zotero em {cfg}, mas aponta para outro comando: {atual}. Use --registrar para trocar.")
        else: print(f"Claude Desktop: conector zotero AUSENTE em {cfg}. Use --registrar para adicionar.")
        return 0 if atual == ENTRADA else 1
    if modo == "--registrar":
        if atual == ENTRADA: print("Claude Desktop: nada a fazer, já registrado."); return 0
        bak = cfg.with_suffix(cfg.suffix + ".bak-pesquisa"); shutil.copy2(cfg, bak)
        d.setdefault("mcpServers", {})["zotero"] = ENTRADA
        cfg.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Claude Desktop: conector zotero registrado em {cfg} (backup em {bak.name}). Reinicie o Claude Desktop."); return 0
    print(__doc__); return 1

if __name__ == "__main__": sys.exit(main(sys.argv))
