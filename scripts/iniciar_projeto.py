#!/usr/bin/env python3
"""Cria (ou complementa) a pasta de um projeto de pesquisa conforme os manuais MirandasTech.

    python3 scripts/iniciar_projeto.py <pasta> --tema "..." [--metodo "..."] [--programa "..."] [--prazo AAAA-MM]

Cria a estrutura de pastas, copia os modelos, gera o PROGRESSO.md único (fases do Pesquisador +
checklists de Método, Uso de IA e Biblioteca) e inicializa o Git. Nunca sobrescreve o que já existe;
se a pasta veio de um dos manuais antigos (PROGRESSO_IA.md, PROGRESSO_METODOLOGIA.md), migra os
itens marcados para o PROGRESSO.md e mantém os arquivos antigos como histórico.
"""
import argparse, re, shutil, subprocess, sys
from datetime import date
from pathlib import Path
AQUI = Path(__file__).resolve().parent.parent; MODELOS = AQUI / "modelos"
ESQUEMA = 1  # versão da estrutura do PROGRESSO.md (fases + checklists M/I/B/L); suba ao mudar tabelas ou colunas
PASTAS = ["00_projeto", "00_protocolo", "01_revisao/fichas", "01_buscas", "02_instrumentos", "02_triagem", "03_etica", "03_extracao",
          "04_sintese", "05_analise", "06_texto", "07_banca", "tools", "dados_FORA_DO_GIT"]
FASES = [
 ("0", "Diagnóstico", "Tema, prazo, programa, orientador e ferramentas registrados; pasta criada", "Pesquisador"),
 ("1", "Pergunta", "Tema delimitado → problema → pergunta com tabela vazia do resultado → objetivos", "Metodólogo"),
 ("2", "Método", "Classificação, desenho, amostra, instrumento, análise; o que a IA pode fazer aqui", "Metodólogo · Orientador"),
 ("3", "Projeto e ética", "Projeto NBR 15287:2025; parecer do CEP quando houver pessoas", "Metodólogo"),
 ("4", "Busca e biblioteca", "Bases, strings verbatim, coleção por base e data; auditoria da biblioteca", "Metodólogo · Bibliotecário"),
 ("5", "Triagem", "Deduplicação, triagem assistida com status preliminar, decisão do aluno, números do PRISMA", "Orientador · Bibliotecário"),
 ("6", "Leitura e síntese", "PDFs do Zotero → notebook; fichamento; matriz de síntese conferida célula a célula", "Leitura (Gemini Notebook)"),
 ("7", "Análise", "Coleta e análise conforme o método; IA só onde autorizada e registrada", "Metodólogo · Orientador"),
 ("8", "Escrita ABNT", "NBR 14724, 10520, 6023 via Zotero; verificação automática de citações e referências", "Bibliotecário · scripts"),
 ("9", "Pré-banca", "Cinco objeções mais fortes, perguntas prováveis, respostas com página", "Metodólogo · Leitura"),
 ("10", "Entrega", "Declaração de uso de IA, backup, versão congelada da biblioteca, checklist final", "Orientador · Bibliotecário"),
]
METODO = [
 ("Pergunta","Pergunta clara, delimitada, empírica e viável; tabela vazia do resultado","7"),("Objetivos","Objetivo geral = pergunta em ação; específicos geram resultado, não etapa","8"),
 ("Justificativa","Lacuna apontada com revisões; relevância; contribuição verificável","9"),("Revisão","Buscas registradas; matriz de síntese; fichas com página","10–11"),
 ("Classificação","Natureza, abordagem, objetivo e procedimento — uma resposta por eixo","12"),("Método","Frase «escolhi X porque…; descartei Y porque…» registrada","14"),
 ("Amostra","População, unidade, amostragem, n calculado e obtido","16"),("Instrumento","Tabela de operacionalização; juízes; pré-teste registrado","18"),
 ("Ética","Parecer do CEP com CAAE antes da coleta; TCLE arquivado; LGPD","6, 27"),("Análise","Técnica decidida antes; pressupostos; efeito com IC; categorias com trecho","21–22"),
 ("Reprodutibilidade","Dados, scripts, ambiente e decisões guardados; figura por script","24"),("Estrutura","NBR 14724:2024 / 15287:2025 e modelo do programa","25, 28"),
 ("Citações","NBR 10520:2023; diretas com página; sem paráfrase próxima","30"),("Referências","NBR 6023:2025 via gerenciador; DOI resolvido; texto ↔ lista","31"),
 ("Texto","Números batem com tabelas; conclusão por objetivo; limites explícitos","32"),("Defesa","Cinco objeções com resposta; ensaio; material à mão","34"),
]
IA = [
 ("Governança","Acordo com o orientador assinado; protocolo congelado e datado antes da primeira busca; procedimento de emenda escrito","6, 17"),
 ("Governança","Arquivo de regras do agente com proibições absolutas, gates humanos e critério de conclusão","37"),
 ("Dados","Dado licenciado e pessoal fora do repositório; treinamento desligado nas ferramentas; hash registrado","9, 11"),
 ("Busca","String de cada base salva verbatim do histórico, com data, filtros, total e SHA-256 do export","18, 22"),
 ("Busca","Teste com e sem truncamento registrado; conjunto-semente com regra de decisão prévia","19, 21"),
 ("Triagem","Codebook versionado; toda recomendação de IA com status preliminar; decisão humana por registro","23, 28"),
 ("Triagem","κ com intervalo de confiança; grau de cegamento declarado; regra de parada do aprendizado ativo escrita antes","26, 27"),
 ("Acesso","Os três números do texto completo medidos separadamente; E5 declarado com lista","31"),
 ("Extração","Cada codificação com página e seção; extração assistida conferida no PDF; dupla codificação em amostra","32, 33"),
 ("Figuras","Toda figura gerada por script que lê o dado; nenhum número digitado; nenhuma imagem gerada por IA","34"),
 ("Referências","Todo DOI resolvido na Crossref na versão final; referência sem DOI com prova alternativa","42"),
 ("Texto","Marcas de IA contadas e removidas; um trecho lido em voz alta; comparação linha a linha com a versão do modelo","40, 41"),
 ("Texto","Todo número do texto bate com a tabela de origem; somas fecham; resumo contado","44"),
 ("Equipe","Registro de uso compartilhado com a coluna «quem»; todos os coautores leram o texto inteiro e aprovaram a declaração","12, 13"),
 ("Declaração","Uso de IA declarado com ferramenta, fase, finalidade, validação e o que a IA não fez","43"),
 ("Entrega","Guia de relato conferido item a item; disponibilidade de dados verdadeira no momento da submissão","16"),
]
BIBLIO = [
 ("Instalação","Zotero instalado do site oficial; Connector no navegador; ícone testado numa página com DOI","6–9"),
 ("Conta","Sincronização automática ligada; decisão sobre arquivos (Storage/WebDAV/nenhum) registrada","10"),
 ("Configurações","Idioma pt-BR; PDF automático e acesso aberto; renomeação automática; pasta de dados fora de nuvem sincronizada","11"),
 ("Estilo","Estilo ABNT instalado e testado com artigo, livro e tese; idioma da citação pt-BR","30–31"),
 ("Editor","Aba/menu Zotero visível no editor; Preferências do documento com ABNT","32–33"),
 ("Estrutura","Coleções por etapa e convenção de etiquetas escritas em DECISOES.md","20–21"),
 ("Auditorias","Pesquisas salvas «sem DOI», «sem PDF», «página da web» criadas","22"),
 ("Auditoria","scripts/auditar_biblioteca.py sem pendências críticas","49"),
 ("Leitura","Convenção de cores das anotações definida; nota extraída com página testada","27–28"),
 ("Exportação","Better BibTeX se houver LaTeX/Obsidian; .bib com «Manter atualizado»","38"),
 ("Backup","Backup da pasta de dados feito com o Zotero fechado; rotina agendada","41"),
 ("Grupo","Se há coautores: grupo privado criado, permissões e dono definidos","44"),
]
LEITURA = [
 ("Conta","Conta pessoal ou institucional escolhida sabendo a diferença de privacidade","7, 43"),
 ("Fontes","PDFs nomeados «Autor - Ano - Título» (do Zotero); nenhuma URL de editora; nenhum PDF escaneado sem OCR","11–14"),
 ("Ingestão","Pergunta de inventário rodada; guia de cada fonte aberto; fontes vazias corrigidas","19"),
 ("Citações","Trecho aberto e lido para cada afirmação usada; frases sem número descartadas","21"),
 ("Matriz","Colunas definidas pelo protocolo; primeira versão pelo notebook; cada célula conferida na planilha","34"),
 ("Dados sensíveis","Nada identificável enviado; transcrições anonimizadas; feedback não enviado em conversas com dados","43–45"),
 ("Declaração","Uso do notebook na leitura declarado; nada do Estúdio citado no texto","45"),
]
def migra(prog_antigo, marcados):
    if prog_antigo.exists():
        for ln in prog_antigo.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\|\s*\d+\s*\|\s*([^|]+)\|\s*([^|]+)\|[^|]*\|\s*\[x\]", ln, re.I)
            if m: marcados.add(m.group(2).strip()[:40])
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("pasta"); ap.add_argument("--tema", default="(a definir)"); ap.add_argument("--metodo", default="(a definir)")
    ap.add_argument("--programa", default="(a definir)"); ap.add_argument("--prazo", default="(a definir)")
    a = ap.parse_args(); raiz = Path(a.pasta).resolve(); raiz.mkdir(parents=True, exist_ok=True)
    for p in PASTAS: (raiz / p).mkdir(parents=True, exist_ok=True)
    def copia(src, dst):
        if not dst.exists(): shutil.copy(src, dst); print("  +", dst.relative_to(raiz))
    for m in ["AGENTS.md", "DECISOES.md", "USO_DE_IA.csv", "ACORDO_ORIENTADOR.md"]: copia(MODELOS / m, raiz / m)
    copia(MODELOS / "registro_exportacoes.csv", raiz / "01_buscas/registro_exportacoes.csv"); copia(MODELOS / "buscas.csv", raiz / "01_buscas/buscas.csv")
    copia(MODELOS / "matriz_sintese.csv", raiz / "04_sintese/matriz_sintese.csv"); copia(MODELOS / "tabela_operacionalizacao.csv", raiz / "02_instrumentos/tabela_operacionalizacao.csv")
    copia(MODELOS / "livro_de_codigos.csv", raiz / "05_analise/livro_de_codigos.csv"); copia(MODELOS / "TCLE_modelo.md", raiz / "03_etica/TCLE.md"); copia(MODELOS / "cronograma.csv", raiz / "00_projeto/cronograma.csv")
    copia(MODELOS / "estrutura_colecoes.md", raiz / "tools/zotero_estrutura_colecoes.md"); copia(MODELOS / "convencao_etiquetas.md", raiz / "tools/zotero_convencao_etiquetas.md")
    copia(MODELOS / "prompts_gemini_notebook.md", raiz / "tools/prompts_gemini_notebook.md"); copia(MODELOS / "estrutura_notebooks.md", raiz / "tools/gemini_notebook_estrutura.md")
    copia(MODELOS / "CODEBOOK.md", raiz / "02_triagem/CODEBOOK.md"); copia(MODELOS / "CONTAGENS.md", raiz / "02_triagem/CONTAGENS.md"); copia(MODELOS / "BUSCA.md", raiz / "01_buscas/BUSCA.md")
    dm = raiz / "00_projeto/DECISOES_METODO.md"
    if not dm.exists(): dm.write_text(f"# Decisões de método — {a.tema}\n\nRegistro da entrevista de decisão com o Metodólogo (uma seção por pergunta, com data).\n\n## Tema delimitado\n\n## Problema e lacuna\n\n## Pergunta e tabela vazia do resultado\n\n## Objetivos\n\n## Hipóteses / pressupostos e variáveis\n\n## Justificativa e delimitação\n\n## Classificação (4 eixos)\n\n## Desenho — «escolhi … porque …; descartei … porque …»\n\n## População, amostra, n\n\n## Técnicas e instrumentos\n\n## Análise\n\n## Ética\n\n## Cronograma e orçamento\n", encoding="utf-8"); print("  +", dm.relative_to(raiz))
    proto = raiz / "00_protocolo/protocolo.md"
    if not proto.exists(): proto.write_text(f"# Protocolo — {a.tema}\n\n**Método:** {a.metodo}\n**Congelado em:** (preencher — depois disso, só por emenda)\n\n1. Pergunta e subperguntas\n2. Bases e justificativa\n3. Blocos conceituais e strings (verbatim)\n4. Janela, idiomas, tipos documentais\n5. Critérios de inclusão e códigos de exclusão\n6. Procedimento de triagem\n7. Conjunto-semente\n8. Campos de extração e codebook\n9. Avaliação de qualidade\n10. Plano de síntese\n11. Gates humanos\n12. Procedimento de emenda\n\n## Emendas\n(nenhuma)\n", encoding="utf-8"); print("  +", proto.relative_to(raiz))
    marcados = set(); migra(raiz / "PROGRESSO_IA.md", marcados); migra(raiz / "PROGRESSO_METODOLOGIA.md", marcados); migra(raiz / "PROGRESSO_ZOTERO.md", marcados)
    prog = raiz / "PROGRESSO.md"
    if prog.exists():
        m = re.search(r"<!-- esquema: (\d+)", prog.read_text(encoding="utf-8")); v = int(m.group(1)) if m else 0
        if v < ESQUEMA: print(f"  ! PROGRESSO.md está no esquema {v} (atual: {ESQUEMA}); nada foi alterado — migração manual: confira as tabelas contra um projeto novo")
        elif v > ESQUEMA: print(f"  ! PROGRESSO.md está no esquema {v}, mais novo que este plugin ({ESQUEMA}); atualize o plugin")
    if not prog.exists():
        L = [f"# Progresso — {a.tema}", f"<!-- esquema: {ESQUEMA} · gerado por iniciar_projeto.py do plugin Pesquisa MirandasTech -->", "", f"**Método provável:** {a.metodo} · **Programa:** {a.programa} · **Prazo:** {a.prazo} · **Início:** {date.today().isoformat()}",
             "Manuais: https://metodologia.mirandastech.com.br/ · https://manual.mirandastech.com.br/ · https://zotero.mirandastech.com.br/ · https://notebook.mirandastech.com.br/", "",
             "Regra: um item só é marcado `[x]` pelo agente responsável depois de conferir a evidência (arquivo, script, número). Anote data e evidência ao lado. O aluno decide; o agente formula e registra em DECISOES.md.", "",
             "## Fases (Pesquisador)", "", "| Fase | Nome | Porta de saída | Quem conduz | Estado | Data | Evidência |", "|---|---|---|---|---|---|---|"]
        for n, nome, porta, quem in FASES: L.append(f"| {n} | {nome} | {porta} | {quem} | [ ] | | |")
        for titulo, itens, pref, manual in [("Método (Metodólogo)", METODO, "M", "metodologia.mirandastech.com.br"), ("Uso de IA (Orientador)", IA, "I", "manual.mirandastech.com.br"),
                                             ("Biblioteca (Bibliotecário)", BIBLIO, "B", "zotero.mirandastech.com.br"), ("Leitura e síntese (Gemini Notebook)", LEITURA, "L", "notebook.mirandastech.com.br")]:
            L += ["", f"## {titulo} — slides em {manual}", "", "| # | Área | Item | Slides | Estado | Data | Evidência conferida |", "|---|---|---|---|---|---|---|"]
            for i, (ar, it, sl) in enumerate(itens, 1):
                est = "[x] (migrado)" if it[:40] in marcados else "[ ]"
                L.append(f"| {pref}{i} | {ar} | {it} | {sl} | {est} | | |")
        prog.write_text("\n".join(L) + "\n", encoding="utf-8"); print("  +", prog.relative_to(raiz), f"({len(marcados)} itens migrados)" if marcados else "")
    gi = raiz / ".gitignore"
    txt = gi.read_text(encoding="utf-8") if gi.exists() else ""
    for linha in ["dados_FORA_DO_GIT/", "dados_restritos_FORA_DO_GIT/", "04_dados_FORA_DO_GIT/", "*.xlsx", "*.xls", "*.pdf", "exports/", ".env"]:
        if linha not in txt: txt = txt.rstrip("\n") + ("\n" if txt else "") + linha + "\n"
    gi.write_text(txt, encoding="utf-8")
    if not (raiz / ".git").exists(): subprocess.run(["git", "init", "-q"], cwd=raiz, check=False)
    print(f"projeto pronto em {raiz}"); print('No Claude Code: "Pesquisador, onde paramos?"  ·  No Codex: /pesquisador onde paramos')
    return 0
if __name__ == "__main__": sys.exit(main())
