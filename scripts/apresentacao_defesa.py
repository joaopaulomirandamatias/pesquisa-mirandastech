#!/usr/bin/env python3
r"""Gera o esqueleto da apresentação de qualificação ou defesa em Beamer (LaTeX) com um slide por bloco do roteiro e o tempo de cada um, e compila se houver LaTeX.

    python3 scripts/apresentacao_defesa.py <pasta_saida> --titulo "…" --autor "…" --orientador "…" --programa "…" --instituicao "…" --tipo qualificacao|defesa --minutos 30 [--capitulos "Introdução;Revisão;Método;Resultados;Discussão;Conclusão"] [--compilar]

Roteiro padrão (proporções do tempo total): abertura e pergunta (10 %), contexto e lacuna (15 %), objetivos (5 %), método (20 %), resultados (30 %), discussão e limites (10 %), conclusão e próximos passos (10 %). Cada frame traz o tempo previsto no rodapé e uma nota do apresentador (`\note{}`) com o que dizer. Regra: um resultado por slide, número com fonte, figura gerada por script. Compila com latexmk (pdflatex) quando `--compilar` e o `latexmk` existir; senão deixa o `.tex` para o Overleaf.
"""
import argparse, shutil, subprocess, sys
from pathlib import Path

ROTEIRO = [("Abertura e pergunta de pesquisa", 0.10, "Quem sou, título, a pergunta em uma frase e por que ela importa."),
           ("Contexto e lacuna", 0.15, "O que já se sabe (3 a 5 referências-chave), o que falta, a lacuna que este trabalho preenche."),
           ("Objetivos", 0.05, "Objetivo geral e específicos, na mesma ordem em que os resultados aparecerão."),
           ("Método", 0.20, "Desenho, participantes/amostra ou corpus, instrumentos, procedimentos, análise; ética (CEP/CAAE) e pré-registro se houver."),
           ("Resultados", 0.30, "Um resultado por slide: tabela ou figura, n, efeito e IC; o número lido em voz alta é o mesmo do texto."),
           ("Discussão e limites", 0.10, "O que os resultados dizem frente à literatura; limitações ditas por você antes que a banca diga."),
           ("Conclusão e próximos passos", 0.10, "Resposta à pergunta, contribuições, o que falta (na qualificação: cronograma até a defesa).")]

def esc(s): return s.replace("&", "\\&").replace("%", "\\%").replace("_", "\\_").replace("#", "\\#")

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pasta"); ap.add_argument("--titulo", required=True); ap.add_argument("--autor", required=True); ap.add_argument("--orientador", default=""); ap.add_argument("--programa", default=""); ap.add_argument("--instituicao", default="")
    ap.add_argument("--tipo", choices=["qualificacao", "defesa"], default="defesa"); ap.add_argument("--minutos", type=int, default=30); ap.add_argument("--capitulos", default=""); ap.add_argument("--compilar", action="store_true")
    a = ap.parse_args(); pasta = Path(a.pasta); pasta.mkdir(parents=True, exist_ok=True)
    evento = "Exame de qualificação" if a.tipo == "qualificacao" else "Defesa"
    frames = []; acumulado = 0.0
    for nome, frac, nota in ROTEIRO:
        minutos = a.minutos * frac; acumulado += minutos
        frames.append(f"\\begin{{frame}}{{{esc(nome)}}}\n  \\begin{{itemize}}\n    \\item [preencher]\n  \\end{{itemize}}\n  \\vfill\\hfill{{\\tiny previsto: {minutos:.1f} min (acumulado {acumulado:.0f} min)}}\n  \\note{{{esc(nota)}}}\n\\end{{frame}}\n")
    if a.capitulos:
        caps = [c.strip() for c in a.capitulos.split(";") if c.strip()]
        frames.insert(1, "\\begin{frame}{Estrutura do trabalho}\n  \\tableofcontents\n\\end{frame}\n")
        for i, c in enumerate(caps): frames.insert(2 + i, f"\\section{{{esc(c)}}}\n")
    tex = f"""\\documentclass[aspectratio=169,11pt]{{beamer}}
\\usetheme{{Boadilla}}
\\usepackage[T1]{{fontenc}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[brazilian]{{babel}}
\\usepackage{{graphicx,booktabs}}
\\setbeamertemplate{{navigation symbols}}{{}}
\\setbeamertemplate{{footline}}[frame number]
\\title{{{esc(a.titulo)}}}
\\subtitle{{{evento} — {esc(a.programa)}}}
\\author{{{esc(a.autor)}{(' \\\\ Orientação: ' + esc(a.orientador)) if a.orientador else ''}}}
\\institute{{{esc(a.instituicao)}}}
\\date{{\\today}}
\\begin{{document}}
\\frame{{\\titlepage}}
{''.join(frames)}
\\begin{{frame}}{{Referências}}
  \\footnotesize [as referências citadas nos slides, no padrão do trabalho]
\\end{{frame}}
\\begin{{frame}}[plain]
  \\centering \\Large Obrigado. \\\\[1em] \\normalsize Perguntas da banca.
\\end{{frame}}
\\end{{document}}
"""
    (pasta / "apresentacao.tex").write_text(tex, encoding="utf-8")
    total = sum(f for _, f, _ in ROTEIRO)
    print(f"gravado: {pasta/'apresentacao.tex'} — {len(ROTEIRO)} blocos para {a.minutos} min ({evento})")
    for nome, frac, _ in ROTEIRO: print(f"  {nome:32} {a.minutos*frac:5.1f} min")
    if a.compilar:
        if not shutil.which("latexmk"): print("latexmk não encontrado: abra apresentacao.tex no Overleaf ou instale o TinyTeX"); return
        r = subprocess.run(["latexmk", "-pdf", "-f", "-interaction=nonstopmode", "apresentacao.tex"], cwd=pasta, capture_output=True, text=True)
        pdf = pasta / "apresentacao.pdf"
        if pdf.exists():
            n = "?"
            if shutil.which("pdfinfo"):
                info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
                for l in info.splitlines():
                    if l.startswith("Pages:"): n = l.split()[-1]
            print(f"ok: {pdf} ({n} páginas)")
        else: print("erro na compilação; veja apresentacao.log"); sys.exit(1)

if __name__ == "__main__": main()
