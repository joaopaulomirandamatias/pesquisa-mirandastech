#!/usr/bin/env python3
"""Cria a pasta de um trabalho acadêmico (TCC, dissertação, tese) a partir do modelo canônico do abnTeX2, já com os seus dados.
    python3 novo_trabalho.py minha-dissertacao --titulo "Título do trabalho" --autor "Nome Sobrenome" \
        --instituicao "Universidade" --orientador "Prof. Dr. Nome" --local "Cidade" --tipo "Dissertação (Mestrado)" --programa "Programa de Pós-Graduação em X"
Precisa do abnTeX2 instalado (o modelo é lido da distribuição TeX: kpsewhich). Gera main.tex, referencias.bib, capitulos/ e compila se latexmk existir."""
import argparse, pathlib, re, shutil, subprocess, datetime
ap = argparse.ArgumentParser(); ap.add_argument("pasta"); ap.add_argument("--titulo", required=True); ap.add_argument("--autor", required=True)
ap.add_argument("--instituicao", default="Universidade"); ap.add_argument("--orientador", default="Prof. Dr. Nome do Orientador"); ap.add_argument("--local", default="Cidade")
ap.add_argument("--tipo", default="Dissertação (Mestrado)"); ap.add_argument("--programa", default="Programa de Pós-Graduação"); ap.add_argument("--data", default=str(datetime.date.today().year))
ap.add_argument("--modelo", help="caminho do abntex2-modelo-trabalho-academico.tex (padrão: procura na distribuição)")
a = ap.parse_args(); raiz = pathlib.Path(a.pasta); raiz.mkdir(parents=True, exist_ok=True); (raiz / "capitulos").mkdir(exist_ok=True); (raiz / "figuras").mkdir(exist_ok=True)
def kps(nome):
    try: return pathlib.Path(subprocess.check_output(["kpsewhich", nome], text=True).strip())
    except Exception: return None
modelo = pathlib.Path(a.modelo) if a.modelo else (kps("abntex2-modelo-trabalho-academico.tex") or pathlib.Path("abntex2-modelo-trabalho-academico.tex"))
if not modelo.exists(): raise SystemExit("modelo não encontrado: passe --modelo com o caminho do abntex2-modelo-trabalho-academico.tex (está no CTAN, pasta doc/examples)")
t = modelo.read_text(encoding="utf-8")
subs = {r"\\titulo\{[^}]*\}": f"\\titulo{{{a.titulo}}}", r"\\autor\{[^}]*\}": f"\\autor{{{a.autor}}}", r"\\local\{[^}]*\}": f"\\local{{{a.local}}}",
        r"\\data\{[^}]*\}": f"\\data{{{a.data}}}", r"\\orientador\{[^}]*\}": f"\\orientador{{{a.orientador}}}", r"\\instituicao\{%?[^}]*\}": f"\\instituicao{{{a.instituicao}}}",
        r"\\tipotrabalho\{[^}]*\}": f"\\tipotrabalho{{{a.tipo}}}"}
for pat, rep in subs.items(): t = re.sub(pat, lambda m: rep, t, count=1, flags=re.S)
pre = f"\\preambulo{{{a.tipo} apresentada ao {a.programa} da {a.instituicao} como requisito parcial para obtenção do título.}}\n"
t = re.sub(r"\\preambulo\{.*?\}\n", lambda m: pre, t, count=1, flags=re.S)
t = t.replace("abntex2-modelo-references", "referencias").replace("abntex2-modelo-img-marca", "figuras/marca")
(raiz / "main.tex").write_text(t, encoding="utf-8")
bib = kps("abntex2-modelo-references.bib") or modelo.parent / "abntex2-modelo-references.bib"; marca = modelo.parent / "abntex2-modelo-img-marca.pdf"
if bib and bib.exists(): shutil.copy(bib, raiz / "referencias.bib")
if marca.exists(): shutil.copy(marca, raiz / "figuras" / "marca.pdf")
print(f"criado: {raiz}/main.tex (dados preenchidos), referencias.bib, capitulos/, figuras/")
if shutil.which("latexmk"):
    r = subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "main.tex"], cwd=raiz, capture_output=True, text=True)
    print("compilado: main.pdf" if (raiz / "main.pdf").exists() else "compilação falhou: veja main.log")
else: print("latexmk não encontrado: envie a pasta ao Overleaf (New Project → Upload Project) ou instale o TinyTeX")
