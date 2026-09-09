#!/usr/bin/env python3
r"""Auditoria de um repositório Git de pesquisa antes de publicar ou entregar.

    python3 scripts/checar_repo.py [pasta]          (padrão: pasta atual)

Confere, só com leitura: se é um repositório Git; arquivos rastreados acima de 50 MiB (aviso do GitHub)
e de 100 MiB (bloqueio); arquivos que costumam guardar segredos (.env, chaves, tokens); padrões de dado
pessoal em arquivos de texto rastreados (CPF, e-mails em massa); pastas de dados que não deveriam estar
no Git; binários pesados que pediriam Git LFS; README, LICENSE, CITATION.cff e .gitignore; remoto
configurado; mudanças sem commit. Não altera nada; imprime OK/AVISO/BLOQUEIO e sai com 1 se houver bloqueio.
"""
import os, re, subprocess, sys
from pathlib import Path

MIB = 1024 * 1024
SEGREDOS_NOME = re.compile(r"(^|/)(\.env(\..*)?|.*\.pem|.*\.key|id_rsa.*|id_ed25519.*|.*\.p12|.*\.pfx|credentials\.json|token.*\.txt)$", re.I)
SEGREDOS_TEXTO = re.compile(r"(ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,}|xox[bp]-[A-Za-z0-9-]{10,}|-----BEGIN (RSA |OPENSSH )?PRIVATE KEY-----)")
CPF = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PASTAS_DADOS = ("dados_FORA_DO_GIT", "dados_brutos", "raw", "entrevistas", "audios", "videos")
BINARIOS = (".pdf", ".docx", ".xlsx", ".pptx", ".zip", ".png", ".jpg", ".jpeg", ".mp4", ".mp3", ".wav", ".sav", ".rds", ".parquet", ".h5", ".pkl")
TEXTO = (".md", ".txt", ".csv", ".tsv", ".json", ".yml", ".yaml", ".tex", ".bib", ".py", ".r", ".R", ".ipynb", ".html", ".xml")

def git(pasta, *args):
    return subprocess.run(["git", "-C", str(pasta), *args], capture_output=True, text=True).stdout

def main():
    pasta = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not (pasta / ".git").exists():
        print(f"BLOQUEIO  {pasta} não é um repositório Git (rode `git init` ou `iniciar_projeto.py`)."); sys.exit(1)
    rastreados = [l for l in git(pasta, "ls-files").splitlines() if l]
    achados = []  # (nivel, texto)
    grandes, enormes, binarios, segredos, pessoais, dados = [], [], [], [], [], []
    for rel in rastreados:
        p = pasta / rel
        if not p.is_file(): continue
        tam = p.stat().st_size
        if tam > 100 * MIB: enormes.append((rel, tam))
        elif tam > 50 * MIB: grandes.append((rel, tam))
        if SEGREDOS_NOME.search(rel): segredos.append(rel)
        if rel.split("/")[0] in PASTAS_DADOS or any(f"/{d}/" in f"/{rel}" for d in PASTAS_DADOS): dados.append(rel)
        if p.suffix.lower() in BINARIOS and tam > 5 * MIB: binarios.append((rel, tam))
        if p.suffix.lower() in TEXTO and tam < 20 * MIB:
            try: t = p.read_text(encoding="utf-8", errors="ignore")
            except Exception: continue
            if SEGREDOS_TEXTO.search(t): segredos.append(rel + " (conteúdo parece token/chave)")
            ncpf = len(CPF.findall(t)); nmail = len(set(EMAIL.findall(t)))
            if ncpf: pessoais.append(f"{rel}: {ncpf} padrão(ões) de CPF")
            if nmail >= 20: pessoais.append(f"{rel}: {nmail} e-mails distintos")
    for rel, tam in enormes: achados.append(("BLOQUEIO", f"{rel} tem {tam/MIB:.0f} MiB — o GitHub recusa acima de 100 MiB; use Git LFS ou tire do Git"))
    for rel, tam in grandes: achados.append(("AVISO", f"{rel} tem {tam/MIB:.0f} MiB — acima de 50 MiB o GitHub avisa; considere Git LFS"))
    for rel in segredos: achados.append(("BLOQUEIO", f"{rel} parece guardar segredo — tire do Git (`git rm --cached`) e troque a credencial"))
    for s in pessoais: achados.append(("AVISO", f"{s} — dado pessoal? LGPD: anonimize ou mantenha fora do Git"))
    for rel in dados: achados.append(("AVISO", f"{rel} está numa pasta de dados brutos — o combinado é ficar fora do Git"))
    if binarios: achados.append(("AVISO", f"{len(binarios)} binário(s) acima de 5 MiB rastreado(s) (ex.: {binarios[0][0]}) — cada versão duplica o tamanho; Git LFS ou fora do Git"))
    for nome, dica in [("README.md", "explique o que é, como reproduzir e como citar"), ("LICENSE", "sem licença ninguém pode reutilizar — choosealicense.com"),
                       ("CITATION.cff", "o GitHub mostra «Cite this repository» — gere com citacao_cff.py"), (".gitignore", "evite subir auxiliares e dados por engano")]:
        if not (pasta / nome).exists(): achados.append(("AVISO", f"falta {nome} — {dica}"))
    if not git(pasta, "remote", "-v").strip(): achados.append(("AVISO", "nenhum remoto configurado — o backup só existe nesta máquina"))
    sujo = [l for l in git(pasta, "status", "--porcelain").splitlines() if l]
    if sujo: achados.append(("AVISO", f"{len(sujo)} arquivo(s) alterado(s) sem commit"))
    ultimo = git(pasta, "log", "-1", "--format=%cs %s").strip()
    print(f"Repositório: {pasta}\n{len(rastreados)} arquivos rastreados · último commit: {ultimo or '(nenhum)'}\n")
    if not achados: print("OK        nada a corrigir: sem arquivos grandes, segredos ou dados pessoais; README, LICENSE, CITATION.cff e .gitignore presentes")
    for nivel, texto in sorted(achados, key=lambda a: a[0] != "BLOQUEIO"): print(f"{nivel:9} {texto}")
    n_b = sum(1 for n, _ in achados if n == "BLOQUEIO"); n_a = len(achados) - n_b
    print(f"\n{n_b} bloqueio(s), {n_a} aviso(s)")
    sys.exit(1 if n_b else 0)

if __name__ == "__main__": main()
