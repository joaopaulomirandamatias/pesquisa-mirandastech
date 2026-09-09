#!/usr/bin/env bash
# Compila um documento LaTeX com latexmk (pdflatex → bibtex/biber → makeindex → pdflatex), tantas vezes quantas forem precisas.
#   bash compilar.sh main.tex            # gera main.pdf
#   bash compilar.sh main.tex --limpar   # apaga os arquivos auxiliares (.aux, .bbl, .log…) antes
#   bash compilar.sh main.tex --xelatex  # usa XeLaTeX (fontes do sistema, abnTeX2 com fontes próprias)
set -e
ARQ="${1:?informe o .tex principal}"; shift || true
MOTOR="-pdf"; for a in "$@"; do case "$a" in --xelatex) MOTOR="-xelatex";; --lualatex) MOTOR="-lualatex";; --limpar) latexmk -C "$ARQ" >/dev/null;; esac; done
command -v latexmk >/dev/null || { echo "latexmk não encontrado: instale o TeX Live/TinyTeX (tlmgr install latexmk)"; exit 1; }
latexmk $MOTOR -f -interaction=nonstopmode -file-line-error "$ARQ" | grep -E "^(Latexmk: (Run number|All targets)|\./.*:[0-9]+: |! )" || true
PDF="${ARQ%.tex}.pdf"; [ -f "$PDF" ] && echo "ok: $PDF ($(pdfinfo "$PDF" 2>/dev/null | awk '/^Pages/{print $2}') páginas)" || { echo "falhou: veja ${ARQ%.tex}.log"; exit 1; }
