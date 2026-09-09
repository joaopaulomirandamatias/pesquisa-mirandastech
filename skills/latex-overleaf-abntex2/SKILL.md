---
name: latex-overleaf-abntex2
description: Escrita do trabalho acadêmico em LaTeX com o abnTeX2 (normas ABNT), no Overleaf ou numa instalação local (TinyTeX/TeX Live) — criar o projeto a partir do modelo canônico, ligar o .bib do Zotero (Better BibTeX), compilar com latexmk, ler o log, conferir citações e gerar PDF. Usar com "LaTeX", "Overleaf", "abnTeX2", "abntex2", "compilar", "bibtex", "erro de compilação", "template ABNT", ".bib".
---

# LaTeX com Overleaf e abnTeX2 — roteiro

Manual: https://latex.mirandastech.com.br/ (páginas públicas do Overleaf e modelos do abnTeX2 compilados de verdade em 09/09/2026). Você prepara o projeto, explica o erro e confere; **o aluno escreve o texto e decide a estrutura**. Nunca faça login no Overleaf pelo aluno nem peça senha; nunca invente comando de pacote que você não conferiu no manual do pacote.

## Regras
- Trabalho acadêmico (TCC, dissertação, tese) → classe `abntex2` com o modelo canônico `abntex2-modelo-trabalho-academico.tex`; artigo → `abntex2-modelo-artigo.tex`; projeto de pesquisa → `abntex2-modelo-projeto-pesquisa.tex`. Se a instituição tem customização própria (lista no wiki do abnTeX2: EESC/USP, ICMC-USP, IME-USP `modelo-latex`, UnB, CEFET-MG, UFSC…), ela vale sobre o canônico.
- Português: `\usepackage[T1]{fontenc}` + `\usepackage[brazilian]{babel}`; UTF-8 é o padrão; pdfLaTeX salvo pedido de fontes do sistema (XeLaTeX/LuaLaTeX).
- Citações pelo `abntex2cite` (`\cite{}` → (SOBRENOME, ano); `\citeonline{}` → Sobrenome (ano)); o `.bib` vem do Zotero com Better BibTeX (chaves estáveis; «Keep updated»). Aviso: o abnTeX2 1.9.7 implementa NBR 6023:2002/10520:2002/14724:2011; as edições vigentes (NBR 6023:2025, 10520:2023, 14724:2024, 15287:2025) têm diferenças — o aluno confere com a biblioteca; `biblatex-abnt` é a alternativa moderna.
- Compilação: `latexmk -pdf -f main.tex` (pdflatex → bibtex → makeindex → pdflatex…); `.log` antigo pode fazer o latexmk pular etapas → `--limpar`/`latexmk -C`. Overleaf: Recompile; «Stop on first error»; tempo de compilação 10 s no plano gratuito (240 s nos pagos).
- No Overleaf gratuito: 1 colaborador, histórico de 24 h, sem Track changes nem integração Zotero — o `.bib` sobe por Upload; nada disso impede entregar a dissertação.

## Scripts (`scripts/`)
- `bash compilar.sh main.tex [--limpar] [--xelatex]` → PDF e contagem de páginas; filtra erros com arquivo:linha.
- `python3 novo_trabalho.py <pasta> --titulo … --autor … --instituicao … --orientador … --local … --tipo "Dissertação (Mestrado)" --programa …` → cria main.tex (dados preenchidos), referencias.bib, capitulos/, figuras/ e compila. Passe `--modelo` com o caminho do modelo do CTAN se a distribuição não trouxer a documentação (TinyTeX).
- `python3 checar_citacoes.py main.tex referencias.bib` → chaves citadas sem entrada (tem de ser 0) e entradas nunca citadas (não entram nas Referências).

## Fluxo com o aluno
1. Escolher Overleaf ou local (TinyTeX: `wget -qO- "https://yihui.org/tinytex/install-bin-unix.sh" | sh`; `tlmgr install abntex2 latexmk`).
2. `novo_trabalho.py` com os dados reais → subir a pasta ao Overleaf («New project → Existing project (.zip)») ou compilar local.
3. Exportar o `.bib` do Zotero (Better BibTeX, Keep updated) para `referencias.bib`; `checar_citacoes.py` antes de cada entrega.
4. Ler o log a cada erro: «Undefined control sequence», «Missing $ inserted», «File not found» (pacote → `tlmgr install`), «Unknown option 'english'» (babel-english).
5. Fechar a fase 8 no `PROGRESSO.md` com o PDF compilado sem `??`, sumário e listas gerados, referências só do que foi citado, e o uso de IA (inclusive AI Assist do Overleaf) declarado.

## Recusas
- «Escreve o capítulo 2 para mim.» → recusa; monta o esqueleto e as perguntas que o capítulo responde.
- «Coloca essa referência que eu lembro de cabeça.» → recusa; busca na base, resolve o DOI, entra pelo Zotero.
- «Deixa o sumário na mão que é mais rápido.» → recusa; sumário e listas vêm do `\tableofcontents`.
- «Entra na minha conta do Overleaf.» → recusa; explica o caminho.
