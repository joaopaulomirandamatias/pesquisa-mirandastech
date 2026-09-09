#!/usr/bin/env python3
"""Mantém os repositórios dos manuais iguais ao plugin nos arquivos compartilhados.
O plugin é a fonte única; cada manual recebe a cópia com as substituições do seu contexto
(checklist próprio em vez do PROGRESSO.md único; caminho da skill em vez de «instalada com o plugin»).

    python3 scripts/sincronizar_manuais.py --verificar [--raiz zotero=/caminho ...]   # só compara; sai 1 se divergir
    python3 scripts/sincronizar_manuais.py --aplicar  [--raiz ...]                     # escreve nos repositórios dos manuais
    python3 scripts/sincronizar_manuais.py --verificar --clonar                        # clona os sete repos do GitHub num diretório temporário (CI)

Sem --raiz, procura os repositórios em ../manual_zotero/repo_publico etc. (estrutura local do autor)."""
import argparse, difflib, os, shutil, subprocess, sys, tempfile
from pathlib import Path

PLUGIN = Path(__file__).resolve().parent.parent
GITHUB = "https://github.com/joaopaulomirandamatias/"
REPOS = {
    "zotero": {"git": "zotero-pesquisa-cientifica", "local": PLUGIN.parent / "manual_zotero/repo_publico",
               "subs": [("PROGRESSO.md (seção «Biblioteca»)", "PROGRESSO_ZOTERO.md"),
                        ("PROGRESSO.md (seção «Método»)", "PROGRESSO_METODOLOGIA.md"),
                        ("PROGRESSO.md (seção «Uso de IA»)", "PROGRESSO_IA.md"),
                        ("a skill `bibliotecario-zotero` (instalada com o plugin)", "`skills/bibliotecario-zotero/SKILL.md` (no plugin) ou `~/.claude/skills/bibliotecario-zotero/SKILL.md`")],
               "arquivos": [("agents/bibliotecario.md", "agents/bibliotecario.md"),
                            ("skills/bibliotecario-zotero/SKILL.md", "skills/bibliotecario-zotero/SKILL.md"),
                            ("scripts/zotero_mcp.py", "scripts/zotero_mcp.py"), ("scripts/auditar_biblioteca.py", "scripts/auditar_biblioteca.py"),
                            ("scripts/exportar_bbt.sh", "scripts/exportar_bbt.sh"), ("scripts/backup_zotero.sh", "scripts/backup_zotero.sh"),
                            ("modelos/convencao_etiquetas.md", "modelos/convencao_etiquetas.md"), ("modelos/estrutura_colecoes.md", "modelos/estrutura_colecoes.md"),
                            ("modelos/estilos/", "modelos/estilos/")]},
    "metodologia": {"git": "metodologia-pesquisa-cientifica", "local": PLUGIN.parent / "manual_metodologia/repo_publico",
               "subs": [("PROGRESSO.md (seção «Método»)", "PROGRESSO_METODOLOGIA.md"),
                        ("PROGRESSO.md (seção «Uso de IA»)", "PROGRESSO_IA.md"),
                        ("PROGRESSO.md (seção «Biblioteca»)", "PROGRESSO_ZOTERO.md"),
                        ("a skill `metodologo-pesquisa` (instalada com o plugin)", "`.claude/skills/metodologo-pesquisa/SKILL.md`")],
               "arquivos": [("agents/metodologo.md", ".claude/agents/metodologo.md"),
                            ("skills/metodologo-pesquisa/SKILL.md", ".claude/skills/metodologo-pesquisa/SKILL.md"),
                            ("skills/projeto-nbr15287/SKILL.md", ".claude/skills/projeto-nbr15287/SKILL.md"),
                            ("skills/abnt-citacoes-referencias/SKILL.md", ".claude/skills/abnt-citacoes-referencias/SKILL.md"),
                            ("skills/banca-simulada/SKILL.md", ".claude/skills/banca-simulada/SKILL.md"),
                            ("scripts/verificar_citacoes.py", "scripts/verificar_citacoes.py"), ("scripts/cronograma.py", "scripts/cronograma.py"),
                            ("scripts/tamanho_amostra.py", "scripts/tamanho_amostra.py"), ("modelos/TCLE_modelo.md", "modelos/TCLE_modelo.md")]},
    "ia": {"git": "ia-na-pesquisa-cientifica", "local": Path.home() / "obsidian/cerebro_digital/40 - Mestrado/Disciplinas/PEA5004 - Sistemas de Automação para Monitoramento e Segurança Pública, Privada e Ambiental para Área Portuária (2026)/repo_publico",
               "subs": [("PROGRESSO.md (seção «Uso de IA»)", "PROGRESSO_IA.md"),
                        ("PROGRESSO.md (seção «Método»)", "PROGRESSO_METODOLOGIA.md"),
                        ("PROGRESSO.md (seção «Biblioteca»)", "PROGRESSO_ZOTERO.md"),
                        ("a skill `orientador-ia-pesquisa` (instalada com o plugin)", "`.claude/skills/orientador-ia-pesquisa/SKILL.md`")],
               "arquivos": [("agents/orientador.md", ".claude/agents/orientador.md"),
                            ("skills/orientador-ia-pesquisa/SKILL.md", ".claude/skills/orientador-ia-pesquisa/SKILL.md"),
                            ("skills/triagem-assistida/SKILL.md", ".claude/skills/triagem-assistida/SKILL.md"),
                            ("scripts/verificar_refs.py", "scripts/verificar_refs.py")]},
    "gemini": {"git": "gemini-notebook-pesquisa-cientifica", "local": PLUGIN.parent / "manual_gemini_notebook/repo_publico",
               "subs": [],
               "arquivos": [("modelos/estrutura_notebooks.md", "modelos/estrutura_notebooks.md"),
                            ("modelos/prompts_gemini_notebook.md", "modelos/prompts.md")]},
    "prisma": {"git": "revisao-sistematica-pesquisa-cientifica", "local": PLUGIN.parent / "manual_prisma/repo_publico",
               "subs": [],
               "arquivos": [("skills/revisao-sistematica-prisma/SKILL.md", "skills/revisao-sistematica-prisma/SKILL.md"),
                            ("scripts/deduplicar.py", "scripts/deduplicar.py"), ("scripts/kappa.py", "scripts/kappa.py"),
                            ("modelos/CONTAGENS.md", "modelos/CONTAGENS.md"), ("modelos/BUSCA.md", "modelos/BUSCA.md"), ("modelos/CODEBOOK.md", "modelos/CODEBOOK.md")]},
    "busca": {"git": "busca-bases-pesquisa-cientifica", "local": PLUGIN.parent / "manual_busca/repo_publico",
               "subs": [],
               "arquivos": [("skills/busca-bases-abertas/SKILL.md", "skills/busca-bases-abertas/SKILL.md"),
                            ("scripts/buscar_openalex.py", "scripts/buscar_openalex.py"), ("scripts/contar_bases.py", "scripts/contar_bases.py"),
                            ("scripts/verificar_oa.py", "scripts/verificar_oa.py"), ("modelos/BUSCA.md", "modelos/BUSCA.md")]},
    "latex": {"git": "latex-overleaf-abntex2-pesquisa-cientifica", "local": PLUGIN.parent / "manual_latex/repo_publico",
               "subs": [],
               "arquivos": [("skills/latex-overleaf-abntex2/SKILL.md", "skills/latex-overleaf-abntex2/SKILL.md"),
                            ("scripts/compilar.sh", "scripts/compilar.sh"), ("scripts/novo_trabalho.py", "scripts/novo_trabalho.py"), ("scripts/checar_citacoes.py", "scripts/checar_citacoes.py")]},
    "git": {"git": "git-github-pesquisa-cientifica", "local": PLUGIN.parent / "manual_git/repo_publico",
               "subs": [],
               "arquivos": [("skills/git-github-pesquisadores/SKILL.md", "skills/git-github-pesquisadores/SKILL.md"),
                            ("scripts/checar_repo.py", "scripts/checar_repo.py"), ("scripts/salvar_versao.sh", "scripts/salvar_versao.sh"), ("scripts/citacao_cff.py", "scripts/citacao_cff.py")]},
    "dados": {"git": "analise-de-dados-pesquisa-cientifica", "local": PLUGIN.parent / "manual_dados/repo_publico",
               "subs": [],
               "arquivos": [("skills/analise-de-dados/SKILL.md", "skills/analise-de-dados/SKILL.md"),
                            ("scripts/limpar_dados.py", "scripts/limpar_dados.py"), ("scripts/analisar.py", "scripts/analisar.py"), ("scripts/codificar_taguette.py", "scripts/codificar_taguette.py")]},
    "bibliometria": {"git": "bibliometria-pesquisa-cientifica", "local": PLUGIN.parent / "manual_bibliometria/repo_publico",
               "subs": [],
               "arquivos": [("skills/bibliometria-vosviewer/SKILL.md", "skills/bibliometria-vosviewer/SKILL.md"),
                            ("scripts/indicadores_bibliometricos.py", "scripts/indicadores_bibliometricos.py"), ("scripts/mapa_vosviewer.py", "scripts/mapa_vosviewer.py")]},
    "cienciaaberta": {"git": "ciencia-aberta-pesquisa-cientifica", "local": PLUGIN.parent / "manual_ciencia_aberta/repo_publico",
               "subs": [],
               "arquivos": [("skills/ciencia-aberta-preregistro/SKILL.md", "skills/ciencia-aberta-preregistro/SKILL.md"),
                            ("scripts/preregistro.py", "scripts/preregistro.py"), ("scripts/deposito_zenodo.py", "scripts/deposito_zenodo.py"), ("scripts/plano_gestao_dados.py", "scripts/plano_gestao_dados.py")]},
    "defesa": {"git": "defesa-qualificacao-pesquisa-cientifica", "local": PLUGIN.parent / "manual_defesa/repo_publico",
               "subs": [],
               "arquivos": [("skills/defesa-qualificacao/SKILL.md", "skills/defesa-qualificacao/SKILL.md"),
                            ("scripts/apresentacao_defesa.py", "scripts/apresentacao_defesa.py"), ("scripts/ensaio_defesa.py", "scripts/ensaio_defesa.py"), ("scripts/checklist_defesa.py", "scripts/checklist_defesa.py")]},
    "orientador": {"git": "manual-do-orientador-pesquisa-cientifica", "local": PLUGIN.parent / "manual_orientador/repo_publico",
               "subs": [],
               "arquivos": [("skills/orientacao-academica/SKILL.md", "skills/orientacao-academica/SKILL.md"),
                            ("scripts/acordo_orientacao.py", "scripts/acordo_orientacao.py"), ("scripts/reuniao_orientacao.py", "scripts/reuniao_orientacao.py"), ("scripts/autoria_credit.py", "scripts/autoria_credit.py"), ("scripts/relatorio_orientador.py", "scripts/relatorio_orientador.py"), ("scripts/resumo_sessao.py", "scripts/resumo_sessao.py")]},
    "professor": {"git": "manual-do-professor-pesquisa-cientifica", "local": PLUGIN.parent / "manual_professor/repo_publico",
               "subs": [],
               "arquivos": [("skills/ensino-pesquisa/SKILL.md", "skills/ensino-pesquisa/SKILL.md"),
                            ("scripts/plano_de_ensino.py", "scripts/plano_de_ensino.py"), ("scripts/rubrica.py", "scripts/rubrica.py"), ("scripts/turma_progresso.py", "scripts/turma_progresso.py")]},
    "submissao": {"git": "submissao-orcid-lattes-pesquisa-cientifica", "local": PLUGIN.parent / "manual_submissao/repo_publico",
               "subs": [],
               "arquivos": [("skills/submissao-orcid-lattes/SKILL.md", "skills/submissao-orcid-lattes/SKILL.md"),
                            ("scripts/checklist_submissao.py", "scripts/checklist_submissao.py"), ("scripts/carta_apresentacao.py", "scripts/carta_apresentacao.py"),
                            ("scripts/resposta_revisores.py", "scripts/resposta_revisores.py"), ("scripts/orcid_lattes_diff.py", "scripts/orcid_lattes_diff.py")]},
}

def transformar(texto, subs):
    for a, b in subs: texto = texto.replace(a, b)
    return texto

def pares(cfg, raiz):
    """(origem no plugin, destino no manual) — expande diretórios."""
    for src, dst in cfg["arquivos"]:
        s = PLUGIN / src
        if src.endswith("/"):
            for f in sorted(s.rglob("*")):
                if f.is_file(): yield f, raiz / dst / f.relative_to(s)
        else: yield s, raiz / dst

def main():
    ap = argparse.ArgumentParser(); g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--verificar", action="store_true"); g.add_argument("--aplicar", action="store_true")
    ap.add_argument("--raiz", action="append", default=[], help="nome=caminho (zotero, metodologia, ia, gemini, prisma, busca, latex, git, dados, bibliometria, cienciaaberta, defesa, orientador, professor)")
    ap.add_argument("--clonar", action="store_true", help="clona os repositórios do GitHub num diretório temporário")
    ap.add_argument("--so", help="só este manual"); a = ap.parse_args()
    raizes = {k: v["local"] for k, v in REPOS.items()}
    for r in a.raiz: k, v = r.split("=", 1); raizes[k] = Path(v)
    tmp = None
    if a.clonar:
        tmp = Path(tempfile.mkdtemp(prefix="sync-manuais-"))
        for k, v in REPOS.items():
            subprocess.run(["git", "clone", "-q", "--depth", "1", GITHUB + v["git"] + ".git", str(tmp / k)], check=True); raizes[k] = tmp / k
    divergentes = 0; ausentes = 0
    for nome, cfg in REPOS.items():
        if a.so and a.so != nome: continue
        raiz = raizes[nome]
        if not raiz.is_dir(): print(f"[{nome}] repositório não encontrado em {raiz} — pulado"); continue
        for src, dst in pares(cfg, raiz):
            if not src.is_file(): print(f"[{nome}] origem ausente no plugin: {src.relative_to(PLUGIN)}"); ausentes += 1; continue
            binario = src.suffix in (".png", ".jpg", ".pdf")
            esperado = src.read_bytes() if binario else transformar(src.read_text(encoding="utf-8"), cfg["subs"]).encode("utf-8")
            atual = dst.read_bytes() if dst.is_file() else None
            if atual == esperado: continue
            divergentes += 1
            if a.aplicar:
                dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(esperado); print(f"[{nome}] atualizado: {dst.relative_to(raiz)}")
            else:
                estado = "AUSENTE" if atual is None else f"{sum(1 for l in difflib.unified_diff(atual.decode('utf-8','replace').splitlines(), esperado.decode().splitlines(), lineterm='') if l[:1] in '+-' and not l.startswith(('+++','---')))} linha(s) diferentes"
                print(f"[{nome}] divergente: {dst.relative_to(raiz)} — {estado}")
    if tmp: shutil.rmtree(tmp, ignore_errors=True)
    if a.verificar:
        print("tudo sincronizado" if not divergentes and not ausentes else f"{divergentes} arquivo(s) divergente(s), {ausentes} ausente(s) no plugin")
        sys.exit(1 if divergentes or ausentes else 0)
    print(f"{divergentes} arquivo(s) escrito(s)")

if __name__ == "__main__": main()
