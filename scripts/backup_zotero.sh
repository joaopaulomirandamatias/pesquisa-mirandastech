#!/usr/bin/env bash
# Backup datado da pasta de dados do Zotero (feche o Zotero antes: copiar com o programa aberto pode corromper o banco).
# Uso: bash backup_zotero.sh [pasta_de_dados] [destino]     Padrões: ~/Zotero  e  ~/Backups
set -e
ORIGEM="${1:-$HOME/Zotero}"; DESTINO="${2:-$HOME/Backups}"
[ -d "$ORIGEM" ] || { echo "Pasta de dados não encontrada: $ORIGEM (veja Configurações → Avançado → Arquivos e pastas)"; exit 1; }
if pgrep -f "[z]otero-bin|[Z]otero.app|[z]otero.exe" >/dev/null; then echo "Feche o Zotero antes de copiar."; exit 1; fi
mkdir -p "$DESTINO"; ARQ="$DESTINO/zotero_$(date +%F_%H%M).tar.gz"
tar -czf "$ARQ" -C "$(dirname "$ORIGEM")" "$(basename "$ORIGEM")"
echo "backup: $ARQ ($(du -h "$ARQ" | cut -f1))"; ls -1t "$DESTINO"/zotero_*.tar.gz | tail -n +8 | xargs -r rm -v   # mantém os 7 mais recentes
