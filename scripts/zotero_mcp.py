#!/usr/bin/env python3
"""Conector MCP da biblioteca Zotero (servidor stdio).

Expõe a biblioteca local do Zotero como ferramentas para Claude Code, Claude Desktop e Codex CLI,
usando a API local (Zotero 7+ aberto, com «Permitir que outros aplicativos neste computador se
comuniquem com o Zotero» ligado em Configurações → Avançado) e, quando o Better BibTeX estiver
instalado, a exportação dele. Só lê a biblioteca; nunca altera nada.

Executar:  uv run --with mcp python zotero_mcp.py        (ou: pip install mcp && python zotero_mcp.py)
"""
import json, re, urllib.parse, urllib.request
try:                                   # mcp 2.x
    from mcp.server.mcpserver import MCPServer as FastMCP
except ImportError:                    # mcp 1.x
    from mcp.server.fastmcp import FastMCP

BASE = "http://127.0.0.1:23119"
mcp = FastMCP("zotero", instructions=(
    "Biblioteca Zotero do usuário, lida pela API local. Use para localizar itens, montar "
    "referências no estilo ABNT, auditar metadados e exportar BibTeX. Nunca invente referências: "
    "se um item não aparece na busca, diga que não está na biblioteca."))

def _get(path, **q):
    url = f"{BASE}{path}" + ("?" + urllib.parse.urlencode(q) if q else "")
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            raw = r.read().decode("utf-8")
            return json.loads(raw) if r.headers.get_content_type() == "application/json" else raw
    except Exception as e:
        raise RuntimeError(f"Zotero não respondeu em {BASE} ({e}). Abra o Zotero e ligue a API local "
                           "em Configurações → Avançado → «Permitir que outros aplicativos…».")

def _todos(path, **q):
    out, start = [], 0
    while True:
        lote = _get(path, limit=100, start=start, **q)
        out += lote
        if len(lote) < 100: return out
        start += 100

def _colecao_id(nome):
    for c in _todos("/api/users/0/collections"):
        if c["data"]["name"].lower() == nome.lower(): return c["key"]
    raise RuntimeError(f"Coleção não encontrada: {nome}")

def _resumo(it):
    d = it["data"]; aut = ", ".join(f"{c.get('lastName','')}" for c in d.get("creators", [])[:3])
    if len(d.get("creators", [])) > 3: aut += " et al."
    return {"chave": it["key"], "tipo": d["itemType"], "titulo": d.get("title", ""), "autores": aut,
            "ano": (re.search(r"\d{4}", d.get("date", "") or "") or [None])[0] if d.get("date") else None,
            "publicacao": d.get("publicationTitle") or d.get("publisher") or "", "doi": d.get("DOI", ""),
            "etiquetas": [t["tag"] for t in d.get("tags", [])]}

@mcp.tool()
def status() -> str:
    """Verifica se o Zotero está aberto com a API local ligada e quantos itens e coleções há."""
    n = len(_todos("/api/users/0/items/top")); c = len(_todos("/api/users/0/collections"))
    return f"Zotero acessível em {BASE}: {n} itens de nível superior, {c} coleções."

@mcp.tool()
def listar_colecoes() -> list[dict]:
    """Lista as coleções da biblioteca (nome, chave, coleção-mãe, número de itens)."""
    return [{"nome": c["data"]["name"], "chave": c["key"], "mae": c["data"].get("parentCollection") or None,
             "itens": c["meta"].get("numItems", 0)} for c in _todos("/api/users/0/collections")]

@mcp.tool()
def buscar_itens(texto: str = "", colecao: str = "", etiqueta: str = "", limite: int = 25) -> list[dict]:
    """Busca itens por texto (título, autor, ano — «Todos os campos»), opcionalmente dentro de uma
    coleção (pelo nome) e/ou com uma etiqueta. Retorna chave, tipo, título, autores, ano, DOI e etiquetas."""
    path = f"/api/users/0/collections/{_colecao_id(colecao)}/items/top" if colecao else "/api/users/0/items/top"
    q = {"limit": max(1, min(limite, 100)), "qmode": "everything"}
    if texto: q["q"] = texto
    if etiqueta: q["tag"] = etiqueta
    return [_resumo(it) for it in _get(path, **q)]

@mcp.tool()
def detalhar_item(chave: str) -> dict:
    """Todos os metadados de um item (pela chave de 8 caracteres) e a lista de anexos e notas."""
    it = _get(f"/api/users/0/items/{chave}"); filhos = _get(f"/api/users/0/items/{chave}/children")
    return {"item": it["data"], "filhos": [{"chave": f["key"], "tipo": f["data"]["itemType"],
            "titulo": f["data"].get("title", ""), "contentType": f["data"].get("contentType", "")} for f in filhos]}

@mcp.tool()
def referencia_abnt(chaves: list[str] | None = None, colecao: str = "", estilo: str = "associacao-brasileira-de-normas-tecnicas",
                    modo: str = "bibliografia") -> str:
    """Gera referências formatadas pelo próprio Zotero (processador CSL). Padrão: estilo ABNT autor-data;
    alternativas: «associacao-brasileira-de-normas-tecnicas-numerico», «apa», «ieee» etc. (precisa estar instalado).
    modo «bibliografia» devolve a lista; modo «citacao» devolve as citações no texto, ex.: (SILVA, 2024)."""
    q = {"format": "bib" if modo == "bibliografia" else "citation", "style": estilo, "locale": "pt-BR", "limit": 100}
    if chaves: path, q["itemKey"] = "/api/users/0/items", ",".join(chaves)
    elif colecao: path = f"/api/users/0/collections/{_colecao_id(colecao)}/items/top"
    else: path = "/api/users/0/items/top"
    raw = _get(path, **q)
    if q["format"] == "bib":
        ents = re.findall(r'<div class="csl-entry"[^>]*>(.*?)</div>', raw, re.S)
        txt = [re.sub(r"<[^>]+>", "", e).replace("&amp;", "&").strip() for e in ents]
        return "\n".join(txt) if txt else raw
    return re.sub(r"<[^>]+>", "", raw)

@mcp.tool()
def auditar(colecao: str = "") -> dict:
    """Aponta o que sai errado na lista de referências: itens sem DOI, sem PDF, sem autor ou ano,
    título em CAIXA ALTA, capturados como «Página da web», anexos órfãos e prováveis duplicados. Só lê."""
    path = f"/api/users/0/collections/{_colecao_id(colecao)}/items/top" if colecao else "/api/users/0/items/top"
    itens = _todos(path); filhos = {}
    for it in _todos("/api/users/0/items"):
        p = it["data"].get("parentItem")
        if p: filhos.setdefault(p, []).append(it["data"])
    CIT = {"journalArticle","book","bookSection","thesis","conferencePaper","report","preprint","standard","statute","document","manuscript","dataset","patent"}
    pend, vistos = [], {}
    for it in itens:
        d = it["data"]; tipo = d["itemType"]; titulo = (d.get("title") or "").strip(); k = it["key"]; p = []
        if tipo in ("attachment", "note"): p.append("anexo/nota sem item pai")
        if tipo == "webpage": p.append("capturado como Página da web")
        if not titulo: p.append("sem título")
        letras = [c for c in titulo if c.isalpha()]
        if len(letras) > 12 and sum(c.isupper() for c in letras) / len(letras) > 0.8: p.append("título em CAIXA ALTA")
        if tipo in CIT and not d.get("creators"): p.append("sem autor")
        if tipo in CIT and not re.search(r"\d{4}", d.get("date", "") or ""): p.append("sem ano")
        doi = (d.get("DOI") or "").strip()
        if tipo in ("journalArticle", "conferencePaper", "preprint", "dataset") and not doi: p.append("sem DOI")
        if doi and not re.match(r"^10\.\S+/\S+$", doi): p.append("DOI mal formado")
        if tipo in CIT and not any(f.get("contentType") == "application/pdf" for f in filhos.get(k, [])): p.append("sem PDF anexado")
        ch = doi.lower() if doi else re.sub(r"\W+", "", titulo.lower())
        if ch:
            if ch in vistos: p.append(f"provável duplicado de {vistos[ch]}")
            else: vistos[ch] = k
        if p: pend.append({"chave": k, "tipo": tipo, "titulo": titulo[:80], "pendencias": p})
    return {"itens_auditados": len(itens), "com_pendencias": len(pend), "pendencias": pend,
            "regra": "Corrija no item do Zotero, nunca na lista do documento (slide 49 do manual)."}

@mcp.tool()
def exportar_bbt(colecao: str, formato: str = "biblatex") -> str:
    """Exporta uma coleção pelo Better BibTeX (formato «bibtex», «biblatex» ou «json» = CSL JSON).
    Exige o plugin Better BibTeX instalado e ativo. Devolve o conteúdo do arquivo."""
    url = f"{BASE}/better-bibtex/export/collection?/{urllib.parse.quote(colecao)}.{formato}"
    try:
        with urllib.request.urlopen(url, timeout=120) as r: return r.read().decode("utf-8")
    except Exception as e:
        raise RuntimeError(f"Exportação BBT falhou ({e}). O Better BibTeX está instalado e a coleção «{colecao}» existe?")

if __name__ == "__main__":
    mcp.run()
