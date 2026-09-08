#!/usr/bin/env python3
"""Confere citações autor-data (NBR 10520:2023) e a consistência texto ↔ lista de referências (NBR 6023:2025).

    python3 scripts/verificar_citacoes.py manuscrito.md

Avisos: (1) citação entre parênteses em CAIXA ALTA — formato antigo; (2) citação direta (aspas) sem página;
(3) autor citado sem entrada na lista; (4) entrada da lista não citada; (5) DOI com formato inválido.
Heurístico: revise os avisos, não os aplique cegamente.
"""
import re, sys
from pathlib import Path
txt = Path(sys.argv[1]).read_text(encoding="utf-8")
m = re.search(r"\n#+\s*Refer[êe]ncias\s*\n", txt, re.I)
corpo, lista = (txt[:m.start()], txt[m.end():]) if m else (txt, "")
avisos = []
for mm in re.finditer(r"\(([A-ZÁÉÍÓÚÂÊÔÃÕÇ]{3,}(?:[;,] ?[A-ZÁÉÍÓÚÂÊÔÃÕÇ]{3,})*),?\s*(\d{4})", corpo):
    avisos.append(("caixa alta (10520:2002)", mm.group(0)))
for mm in re.finditer(r"[“\"][^”\"]{25,}[”\"]\s*\(([^)]*\d{4}[^)]*)\)", corpo):
    if not re.search(r"p\.\s*\d", mm.group(1)): avisos.append(("citação direta sem página", mm.group(0)[-80:]))
cit = set(); 
for mm in re.finditer(r"\(([A-ZÀ-Ý][\wÀ-ÿ'\- ]+?)(?: et al\.)?(?:;\s*[A-ZÀ-Ý][\wÀ-ÿ'\- ]+?)*,\s*(\d{4})", corpo): cit.add((mm.group(1).split(";")[0].strip().lower(), mm.group(2)))
for mm in re.finditer(r"\b([A-ZÀ-Ý][\wÀ-ÿ'\-]+)(?: e [A-ZÀ-Ý][\wÀ-ÿ'\-]+)?(?: et al\.)? \((\d{4})", corpo): cit.add((mm.group(1).lower(), mm.group(2)))
ent = set()
for linha in lista.splitlines():
    mm = re.match(r"\s*([A-ZÀ-Ý][A-ZÀ-Ý'\- ]+),", linha)
    y = re.search(r"\b(19|20)\d{2}\b", linha)
    if mm and y: ent.add((mm.group(1).split()[0].lower(), y.group(0)))
for c in sorted(cit):
    if lista and not any(c[0].startswith(e[0][:6]) and c[1] == e[1] for e in ent): avisos.append(("citado sem entrada na lista", f"{c[0].title()}, {c[1]}"))
for e in sorted(ent):
    if not any(c[0].startswith(e[0][:6]) and c[1] == e[1] for c in cit): avisos.append(("na lista, não citado no texto", f"{e[0].upper()}, {e[1]}"))
for mm in re.finditer(r"(?i)doi:?\s*([^\s]+)", lista):
    if not re.match(r"(https?://doi\.org/)?10\.\d{4,9}/\S+", mm.group(1)): avisos.append(("DOI inválido", mm.group(0)))
print(f"citações no texto: {len(cit)} · entradas na lista: {len(ent)} · avisos: {len(avisos)}")
for tipo, tr in avisos: print(f"  [{tipo}] {tr}")
sys.exit(1 if avisos else 0)
