#!/usr/bin/env bash
# Salva uma versão do trabalho: mostra o que mudou, faz o commit e, se pedido, marca uma tag anotada.
#   bash scripts/salvar_versao.sh "mensagem do commit" [--tag v1.0 "descrição da versão"]
# Recusa se algum arquivo acima de 100 MiB estiver para entrar (o GitHub bloqueia). Não faz push: mostra o comando.
set -e
MSG="${1:?uso: salvar_versao.sh \"mensagem\" [--tag vX.Y \"descrição\"]}"; shift || true
TAG=""; TAGMSG=""
if [ "${1:-}" = "--tag" ]; then TAG="${2:?informe a tag, ex.: v1.0}"; TAGMSG="${3:-$TAG}"; fi
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "erro: esta pasta não é um repositório Git (git init)"; exit 1; }
git add -A
if git diff --cached --quiet; then echo "nada mudou desde o último commit"; exit 0; fi
echo "Mudanças que entram nesta versão:"; git diff --cached --stat | tail -n 15
GRANDE=$(git diff --cached --name-only --diff-filter=AM | while read -r f; do [ -f "$f" ] && [ "$(stat -c %s "$f")" -gt 104857600 ] && echo "$f"; done || true)
if [ -n "$GRANDE" ]; then echo "recusado: arquivo(s) acima de 100 MiB — o GitHub bloqueia:"; echo "$GRANDE"; git reset -q; exit 1; fi
git commit -q -m "$MSG"
echo; git log -1 --format="commit %h · %cs · %s"
if [ -n "$TAG" ]; then git tag -a "$TAG" -m "$TAGMSG"; echo "tag $TAG criada: $TAGMSG"; fi
if git remote get-url origin >/dev/null 2>&1; then echo "para enviar: git push --follow-tags"; else echo "sem remoto ainda: crie o repositório no GitHub e rode  git remote add origin <url>  e  git push -u origin main"; fi
