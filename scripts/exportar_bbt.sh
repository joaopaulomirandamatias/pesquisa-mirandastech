#!/usr/bin/env bash
# Exporta uma coleção pelo Better BibTeX (Zotero aberto, BBT instalado) sem abrir menus.
# Uso: bash exportar_bbt.sh "Nome da coleção" [bibtex|biblatex|json] [saida.bib]
set -e
COL="${1:?informe o nome da coleção}"; FMT="${2:-biblatex}"; OUT="${3:-referencias.bib}"
URL="http://127.0.0.1:23119/better-bibtex/export/collection?/$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$COL").$FMT"
curl -sf "$URL" -o "$OUT" && echo "exportado: $OUT ($(grep -c '^@' "$OUT" 2>/dev/null || echo ?) entradas)"
