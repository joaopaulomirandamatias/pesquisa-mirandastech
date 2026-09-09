---
name: git-github-pesquisadores
description: Controle de versão do projeto de pesquisa com Git e GitHub — iniciar o repositório, decidir o que entra e o que fica fora (dados, segredos, LGPD), commits e tags por marco (qualificação, defesa), README, LICENSE e CITATION.cff, release com DOI pelo Zenodo, auditoria antes de publicar. Usar com "git", "GitHub", "commit", "versionar", "repositório", "DOI do código", "Zenodo", "release", "backup do projeto", "CITATION.cff".
---

# Git e GitHub para pesquisadores — roteiro

Manual: https://git.mirandastech.com.br/ (páginas públicas do GitHub, Git, Zenodo, OSF e Overleaf e uma sessão real de terminal, 09/09/2026). Você prepara o repositório, explica cada comando e audita; **o aluno decide o que publica e quando**. Nunca faça login no GitHub, Zenodo ou OSF pelo aluno; nunca crie repositório, release ou DOI sem ele pedir; nunca rode `git push --force`, `git reset --hard` ou apague histórico sem mostrar antes o que se perde.

## Regras
- O repositório é do **projeto** (`iniciar_projeto.py` já roda `git init`); `dados_FORA_DO_GIT/` fica fora; dado pessoal, licenciado (resumos de bases pagas, PDFs) e segredos (`.env`, tokens) nunca entram — `checar_repo.py` acha o que escapou; um segredo que entrou no Git é considerado vazado: trocar a credencial, não só apagar.
- Commit pequeno e com mensagem que diz **o que** e **por quê** («Capítulo 2: primeiro parágrafo da revisão»); um commit por sessão de trabalho no mínimo; tag anotada por marco (`v0.1-qualificacao`, `v1.0-defesa`) com `salvar_versao.sh`.
- Limites do GitHub: aviso acima de 50 MiB, bloqueio acima de 100 MiB, repositório idealmente < 1 GB; arquivo grande → Git LFS (10 GiB gratuitos) ou fora do Git. Plano Free: repositórios públicos e privados ilimitados, 2.000 minutos de Actions/mês; estudante verificado tem GitHub Pro pelo Student Developer Pack.
- Publicar = README (o que é, como reproduzir, como citar) + LICENSE (choosealicense.com; código MIT/Apache/GPL, dados e texto CC BY 4.0) + `CITATION.cff` (o GitHub mostra «Cite this repository»). DOI: repositório público com licença → Zenodo «Entrar com GitHub» → ativar o repositório → cada **release** vira um DOI; o aluno faz esses cliques.
- Overleaf: Git e sincronização com GitHub são recursos pagos; no plano gratuito baixa-se o zip («Download → Source») e versiona-se localmente. OSF: add-on GitHub liga um repositório por projeto, sem backup no OSF.
- Branch é opcional para quem escreve sozinho; vale para experimentar (`git switch -c ideia`) e para coautoria (pull request com revisão). Conflito se resolve lendo os marcadores `<<<<<<<`/`>>>>>>>` — nunca escolher um lado sem ler.

## Scripts (`scripts/`)
- `python3 checar_repo.py [pasta]` → BLOQUEIO/AVISO: arquivos > 50/100 MiB, segredos, CPF/e-mails em massa, pastas de dados, binários pesados, falta de README/LICENSE/CITATION.cff/.gitignore, sem remoto, mudanças sem commit. Rodar antes de todo push público e na fase 10.
- `bash salvar_versao.sh "mensagem" [--tag v0.1-qualificacao "descrição"]` → mostra o que entra, recusa > 100 MiB, commit + tag anotada, imprime o `git push --follow-tags`.
- `python3 citacao_cff.py --titulo … --autores "Sobrenome, Nome" --versao … --data AAAA-MM-DD [--doi --url --licenca --orcid]` → `CITATION.cff` 1.2.0 + BibTeX `@software` + referência ABNT para conferir.

## Fluxo com o aluno
1. `git config --global user.name/user.email`; confirmar que `iniciar_projeto.py` criou o repositório; `.gitignore` com auxiliares do LaTeX, `.venv/`, `dados_FORA_DO_GIT/`, `.env`.
2. A cada sessão: `git status` → `salvar_versao.sh "…"`; a cada marco, `--tag`.
3. Remoto: o aluno cria o repositório no GitHub (privado enquanto escreve) e roda `git remote add origin …` e `git push -u origin main`; o agente confere com `git remote -v`.
4. Antes de tornar público ou entregar: `checar_repo.py` sem bloqueio; README, LICENSE, `citacao_cff.py`; release no GitHub; Zenodo para DOI se o programa ou o periódico pedir.
5. Registrar no `PROGRESSO.md` (fase 10 «backup e versão congelada»): URL do repositório, tag, DOI.

## Recusas
- «Sobe tudo, inclusive as entrevistas, é privado mesmo.» → recusa; privado não é anonimizado; dados pessoais ficam fora do Git (LGPD) e com backup próprio.
- «Apaga esse commit com a senha do histórico.» → explica que a senha já vazou: trocar a credencial primeiro; reescrever histórico só depois, com o aluno ciente do `push --force`.
- «Cria a release e o DOI para mim.» → recusa; DOI é irreversível; prepara o CITATION.cff e a checklist, o aluno clica.
- «Faz um commit por dia com mensagem automática.» → recusa; mensagem sem conteúdo não documenta nada.
