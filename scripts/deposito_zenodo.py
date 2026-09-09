#!/usr/bin/env python3
r"""Prepara um depósito no Zenodo (ou repositório compatível): confere a pasta, gera o `.zenodo.json` (metadados lidos pelo Zenodo em uploads do GitHub) e um checklist FAIR.

    python3 scripts/deposito_zenodo.py <pasta> --titulo "…" --autores "Sobrenome, Nome; …" --tipo dataset|software|publication|other --licenca CC-BY-4.0 [--descricao "…"] [--palavras "a;b;c"] [--orcid "0000-…;…"] [--afiliacao "Instituição"]

Confere: tamanho total e maior arquivo (o Zenodo aceita até 50 GB por registro e 100 arquivos por upload), README presente, arquivos com cara de dado pessoal ou segredo (usa os mesmos padrões do checar_repo.py, em modo simples), formatos abertos (csv/txt/json/ods/pdf) × proprietários (xlsx/docx/sav). Grava `.zenodo.json` (title, creators com name/affiliation/orcid, description, upload_type, license, keywords, access_right open) e imprime o checklist FAIR (F1–R1.3) com o que já está atendido. Não envia nada: o upload e o botão «Publish» são do aluno (o DOI é irreversível).
"""
import argparse, json, os, re, sys
from pathlib import Path

GB = 1024 ** 3; MIB = 1024 ** 2
ABERTOS = {".csv", ".txt", ".json", ".ods", ".pdf", ".md", ".tex", ".bib", ".png", ".svg", ".tsv", ".xml", ".html", ".py", ".r", ".R", ".ipynb", ".yaml", ".yml"}
PROPRIETARIOS = {".xlsx", ".xls", ".docx", ".doc", ".sav", ".pptx", ".psd", ".mat"}
SEGREDO = re.compile(r"(^|/)(\.env(\..*)?|.*\.pem|.*\.key|id_rsa.*|credentials\.json)$", re.I); CPF = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pasta"); ap.add_argument("--titulo", required=True); ap.add_argument("--autores", required=True); ap.add_argument("--tipo", choices=["dataset", "software", "publication", "other"], required=True)
    ap.add_argument("--licenca", default="CC-BY-4.0"); ap.add_argument("--descricao", default=""); ap.add_argument("--palavras", default=""); ap.add_argument("--orcid", default=""); ap.add_argument("--afiliacao", default="")
    a = ap.parse_args(); pasta = Path(a.pasta).resolve()
    arquivos = [p for p in pasta.rglob("*") if p.is_file() and ".git" not in p.parts]
    total = sum(p.stat().st_size for p in arquivos); maior = max(arquivos, key=lambda p: p.stat().st_size) if arquivos else None
    avisos = []
    if not arquivos: sys.exit("pasta vazia")
    if total > 50 * GB: avisos.append(f"BLOQUEIO total {total/GB:.1f} GB > 50 GB por registro")
    if len(arquivos) > 100: avisos.append(f"AVISO {len(arquivos)} arquivos > 100 por upload: compacte em .zip por tipo")
    if not any(p.name.lower().startswith("readme") for p in arquivos): avisos.append("AVISO falta README (o que é, como foi coletado, variáveis/dicionário de dados, como citar)")
    prop = [p for p in arquivos if p.suffix.lower() in PROPRIETARIOS]
    if prop: avisos.append(f"AVISO {len(prop)} arquivo(s) em formato proprietário (ex.: {prop[0].name}) — inclua também uma versão aberta (csv/ods/pdf)")
    for p in arquivos:
        if SEGREDO.search(str(p.relative_to(pasta))): avisos.append(f"BLOQUEIO {p.relative_to(pasta)} parece segredo")
        if p.suffix.lower() in {".csv", ".txt", ".json", ".tsv", ".md"} and p.stat().st_size < 20 * MIB:
            t = p.read_text(encoding="utf-8", errors="ignore")
            if CPF.search(t): avisos.append(f"BLOQUEIO {p.relative_to(pasta)} contém padrão de CPF — anonimize antes de depositar")
    autores = []
    orcids = [x.strip() for x in a.orcid.split(";")] if a.orcid else []
    for i, x in enumerate([x.strip() for x in a.autores.split(";") if x.strip()]):
        if "," not in x: sys.exit('erro: autores como "Sobrenome, Nome; …"')
        c = {"name": x}
        if a.afiliacao: c["affiliation"] = a.afiliacao
        if i < len(orcids) and orcids[i]: c["orcid"] = orcids[i]
        autores.append(c)
    meta = {"title": a.titulo, "upload_type": a.tipo, "description": a.descricao or "[preencher: o que é, como foi produzido, como reutilizar, como citar]", "creators": autores,
            "access_right": "open", "license": a.licenca.lower(), "keywords": [k.strip() for k in a.palavras.split(";") if k.strip()]}
    (pasta / ".zenodo.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Pasta: {pasta}\n{len(arquivos)} arquivos, {total/MIB:.1f} MiB no total; maior: {maior.relative_to(pasta)} ({maior.stat().st_size/MIB:.1f} MiB)")
    print(f"gravado: {pasta/'.zenodo.json'}\n")
    for v in sorted(avisos, key=lambda s: not s.startswith("BLOQUEIO")): print(v)
    if not avisos: print("OK        nada a corrigir antes do upload")
    tem_readme = any(p.name.lower().startswith("readme") for p in arquivos)
    fair = [("F1 identificador persistente", "o Zenodo atribui o DOI ao publicar (reserve antes para citar no texto)"),
            ("F2 metadados ricos", "título, autores, descrição, palavras-chave" + (" — descrição ainda [preencher]" if not a.descricao else " ✔")),
            ("F4 indexado em recurso pesquisável", "Zenodo é indexado (OpenAIRE, Google Dataset Search) ✔"),
            ("A1 recuperável por protocolo aberto", "HTTPS/DOI ✔"), ("A2 metadados persistem mesmo sem arquivos", "política do Zenodo ✔"),
            ("I1/I2 formatos e vocabulários abertos", "formatos abertos" + (" ✔" if not prop else " — há proprietários (ver aviso)")),
            ("R1.1 licença clara", f"{a.licenca} ✔"), ("R1.2 proveniência", "README com origem, método e versão" + (" ✔" if tem_readme else " — falta README")), ("R1.3 padrões da área", "[conferir: dicionário de dados, unidades, codebook]")]
    print("\nChecklist FAIR:"); [print(f"  {k:42} {v}") for k, v in fair]
    print("\nPróximos passos (do aluno): zenodo.org → Upload → New upload → arrastar os arquivos → preencher (o .zenodo.json serve de guia) → Reserve DOI → Preview → Publish.")

if __name__ == "__main__": main()
