#!/usr/bin/env python3
"""Gera HTML autônomo e PDF a partir de mirandastech_plugin.html."""
import re, sys, time
from pathlib import Path
AQUI=Path(__file__).resolve().parent
FONTE=AQUI/"mirandastech_plugin.html"
HTML=AQUI/"Manual_Plugin_Pesquisa_Claude_Codex_MirandasTech.html"
PDF=AQUI/"Manual_Plugin_Pesquisa_Claude_Codex_MirandasTech.pdf"
frag=FONTE.read_text(encoding="utf-8"); frag.encode("utf-8")
frag=re.sub(r'^<meta charset="utf-8">\s*','',frag)
m=re.search(r'<title>(.*?)</title>\s*',frag); titulo=m.group(1); frag=frag.replace(m.group(0),'',1)
k=frag.index('</style>')+len('</style>')
doc=('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n'
     f'<title>{titulo}</title>\n{frag[:k]}\n</head>\n<body>\n{frag[k:]}\n</body>\n</html>\n')
HTML.write_text(doc,encoding="utf-8"); print("html",HTML.name,f"{HTML.stat().st_size:,}")
if "--so-html" not in sys.argv:
    from weasyprint import HTML as W
    t=time.time(); W(str(HTML)).write_pdf(str(PDF)); print("pdf",PDF.name,f"{PDF.stat().st_size:,}",f"({time.time()-t:.0f}s)")
