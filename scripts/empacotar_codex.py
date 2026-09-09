#!/usr/bin/env python3
"""Gera o ZIP do plugin para o diretório do Codex/ChatGPT (platform.openai.com/plugins → Create plugin → Skills only).

    python3 scripts/empacotar_codex.py                 # usa a versão do .codex-plugin/plugin.json
    python3 scripts/empacotar_codex.py --versao 1.1.0  # atualiza a versão nos dois manifestos antes de empacotar

O ZIP contém só o que o Codex precisa (manifesto, ícones, skills, scripts, modelos, prompts, AGENTS.md, README, LICENSE),
sem .git, cache Python nem arquivos do plugin do Claude Code. Antes de empacotar, valida os manifestos e o frontmatter
das skills — os mesmos erros que o portal apontaria.
"""
import argparse, json, re, sys, zipfile
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent
INCLUIR = [".codex-plugin", "assets", "skills", "scripts", "modelos", "codex", "AGENTS.md", "README.md", "LICENSE"]
EXCLUIR = {"__pycache__", ".DS_Store"}
def erro(msg): print("ERRO:", msg); sys.exit(1)
def validar(manifesto):
    for chave in ["name", "version", "description", "skills"]:
        if chave not in manifesto: erro(f"plugin.json sem o campo «{chave}»")
    iface = manifesto.get("interface", {})
    for chave in ["displayName", "shortDescription", "longDescription", "developerName", "category", "composerIcon", "logo"]:
        if not iface.get(chave): erro(f"interface.{chave} ausente — o portal recusa sem ele")
    if len(iface["shortDescription"]) > 30: erro(f"interface.shortDescription tem {len(iface['shortDescription'])} caracteres; o portal aceita até 30")
    for chave in ["composerIcon", "logo"]:
        f = RAIZ / iface[chave]
        if not f.exists(): erro(f"{chave}: arquivo não encontrado: {iface[chave]}")
        with open(f, "rb") as fh:
            cab = fh.read(24)
            if cab[:8] != b"\x89PNG\r\n\x1a\n": erro(f"{chave} não é PNG")
            w, h = int.from_bytes(cab[16:20], "big"), int.from_bytes(cab[20:24], "big")
            if w != h: erro(f"{chave} não é quadrado ({w}x{h})")
            if w < (48 if chave == "composerIcon" else 256): erro(f"{chave} pequeno demais ({w}px)")
    if not re.match(r"^\d+\.\d+\.\d+$", manifesto["version"]): erro("version deve ser X.Y.Z")
    for sk in sorted((RAIZ / "skills").glob("*/SKILL.md")):
        t = sk.read_text(encoding="utf-8")
        if not (t.startswith("---") and "\nname:" in t.split("---")[1] and "\ndescription:" in t.split("---")[1]): erro(f"{sk.relative_to(RAIZ)} sem frontmatter name/description")
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--versao"); ap.add_argument("--saida", default=None); a = ap.parse_args()
    pj = RAIZ / ".codex-plugin/plugin.json"; m = json.loads(pj.read_text(encoding="utf-8"))
    if a.versao:
        m["version"] = a.versao; pj.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        cj = RAIZ / ".claude-plugin/plugin.json"; c = json.loads(cj.read_text(encoding="utf-8")); c["version"] = a.versao; cj.write_text(json.dumps(c, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        mk = RAIZ / ".claude-plugin/marketplace.json"; k = json.loads(mk.read_text(encoding="utf-8"))
        for p in k.get("plugins", []):
            if p.get("name") == c["name"]: p["version"] = a.versao
        mk.write_text(json.dumps(k, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"); print(f"versão {a.versao} gravada nos manifestos do Codex e do Claude Code")
    validar(m)
    nome = m["name"]; saida = Path(a.saida) if a.saida else RAIZ / "dist" / f"{nome}-{m['version']}.zip"; saida.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as z:
        for item in INCLUIR:
            p = RAIZ / item
            if not p.exists(): erro(f"não encontrado: {item}")
            arquivos = [p] if p.is_file() else [f for f in p.rglob("*") if f.is_file()]
            for f in arquivos:
                if EXCLUIR & set(f.relative_to(RAIZ).parts): continue
                z.write(f, f"{nome}/{f.relative_to(RAIZ).as_posix()}"); n += 1
    nome = saida.relative_to(RAIZ) if saida.is_relative_to(RAIZ) else saida
    print(f"ok: {nome} — {n} arquivos, {saida.stat().st_size/1024:.0f} KB, versão {m['version']}")
    print("Envie em platform.openai.com/plugins → Create plugin → Skills only (nova versão = novo envio).")
if __name__ == "__main__": main()
