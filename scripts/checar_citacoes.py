#!/usr/bin/env python3
r"""Confere as citações de um projeto LaTeX contra o .bib: chaves citadas que não existem no .bib e entradas do .bib nunca citadas.
    python3 checar_citacoes.py main.tex referencias.bib
Segue \input e \include; entende \cite, \citeonline, \citep, \citet, \parencite, \textcite, \autocite, \nocite (várias chaves separadas por vírgula)."""
import re, sys, pathlib
def coletar_tex(p, vistos):
    p = pathlib.Path(p)
    if p.suffix == "": p = p.with_suffix(".tex")
    if not p.exists() or p in vistos: return ""
    vistos.add(p); t = p.read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"(?<!\\)%.*", "", t)
    for m in re.finditer(r"\\(?:input|include)\{([^}]+)\}", t): t += coletar_tex(p.parent / m.group(1), vistos)
    return t
tex, bib = sys.argv[1], sys.argv[2]
t = coletar_tex(tex, set())
citadas = set()
for m in re.finditer(r"\\(?:no)?cite[a-zA-Z*]*(?:\[[^\]]*\]){0,2}\{([^}]+)\}", t):
    for k in m.group(1).split(","): citadas.add(k.strip())
bibtxt = pathlib.Path(bib).read_text(encoding="utf-8", errors="replace")
chaves = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bibtxt))
faltam = sorted(citadas - chaves); sobram = sorted(chaves - citadas)
print(f"citadas no texto: {len(citadas)} · entradas no .bib: {len(chaves)}")
print(f"citadas sem entrada no .bib ({len(faltam)}): {', '.join(faltam) or '—'}")
print(f"no .bib e nunca citadas ({len(sobram)}): {', '.join(sobram[:15])}{' …' if len(sobram) > 15 else '' if sobram else '—'}")
sys.exit(1 if faltam else 0)
