---
name: bibliometria-vosviewer
description: Análise bibliométrica e mapeamento científico do corpus da busca — indicadores (produção por ano, fontes, autores, citações, índice h do corpus), redes de coautoria, coocorrência de termos, fontes e acoplamento bibliográfico nos formatos do VOSviewer e do VOSviewer Online; Bibliometrix/biblioshiny como alternativa em R; relato responsável (Manifesto de Leiden, DORA). Usar com "bibliometria", "VOSviewer", "Bibliometrix", "biblioshiny", "mapa de coautoria", "coocorrência de palavras-chave", "acoplamento bibliográfico", "cocitação", "índice h", "análise de citações".
---

# Bibliometria com VOSviewer e Bibliometrix — roteiro

Manual: https://bibliometria.mirandastech.com.br/ (corpus real de 236 documentos do OpenAlex, mapas abertos de verdade no VOSviewer Online em 09/09/2026). Você constrói os arquivos, abre os mapas e explica o que cada rede mede; **o aluno decide o corpus, os limiares e a interpretação**. Nunca use indicador de citação para «avaliar» pessoas; bibliometria aqui descreve um campo, não julga pesquisadores (Manifesto de Leiden, DORA).

## Regras
- O corpus vem da busca registrada (fase 4, `busca-bases-abertas`): mesma string, mesma data, mesmo arquivo; um mapa sem diário de busca não é reprodutível. Nunca misture exportações de bases diferentes num mesmo mapa (o VOSviewer não permite).
- Cada mapa declara: tipo de link (coautoria, coocorrência, citação, acoplamento, cocitação), unidade (autor, termo, fonte, documento), contagem (completa ou fracionada), limiar mínimo, número de itens, links e clusters, e a data da extração.
- Coautoria e citação dependem de desambiguação de nomes: conferir variantes («Silva, J.» e «Silva, João»), usar o thesaurus do VOSviewer; nomes de organizações como autor («AMC Instruments») são erro da base a corrigir.
- Termos de título e resumo são em inglês no VOSviewer; corpus em português exige mapa de palavras-chave da base ou tradução declarada.
- Citações do Crossref contam só o que o Crossref indexa (menos que Scopus/WoS); dizer a fonte e a data de todo número. Índice h «do corpus» não é o índice h de ninguém.
- Preprints, teses e datasets em repositórios (Zenodo, SSRN, arXiv) aparecem como «fonte»: separar por tipo antes de falar em «periódicos mais produtivos».
- Interpretação: cluster ≠ tema pronto; ler os documentos de cada cluster antes de nomeá-lo; um mapa ilustra a revisão, não a substitui.

## Scripts (`scripts/`)
- `python3 indicadores_bibliometricos.py corpus.csv [--citacoes crossref_refs.json] [--top N] [--figura producao.png] [--markdown indicadores.md]` → total, período, produção por ano (figura por script), fontes, autores, tipos, acesso aberto, mais citados e índice h do corpus.
- `python3 mapa_vosviewer.py corpus.csv --tipo coautoria|termos|fontes|acoplamento [--refs crossref_refs.json] --min N --saida nome` → `nome_map.txt`, `nome_network.txt` (VOSviewer: File → Open) e `nome.json` (VOSviewer Online: botão Open → «VOSviewer JSON file»).
- Enriquecimento de citações e referências pelo Crossref: `api.crossref.org/works/<DOI>` com `mailto` (polite pool), guardando `doi`, `citacoes`, `refs_doi` num JSON.

## Fluxo com o aluno
1. Confirmar o corpus (CSV com title, abstract, year, doi, authors, source) e o diário da busca.
2. `indicadores_bibliometricos.py` → ler com o aluno: o que cresce, onde se publica, quem publica; corrigir nomes/organizações.
3. `mapa_vosviewer.py` para cada pergunta (quem colabora, quais temas, quais fontes, quais documentos compartilham referências) → abrir no VOSviewer (desktop) ou no VOSviewer Online → ajustar limiar até o mapa ser legível (dezenas, não centenas de itens) → exportar a figura pelo próprio VOSviewer.
4. Escrever a seção de método bibliométrico (base, string, data, n, software e versão, tipo de link, contagem, limiares) e a leitura dos clusters com exemplos de documentos.
5. Registrar no `PROGRESSO.md` (fase 6/7) os arquivos gerados e a data.

## Recusas
- «Ranqueia os autores para eu dizer quem é o melhor.» → recusa; produção ≠ qualidade (Leiden, DORA); mostra produção e colaboração, sem juízo.
- «Junta a exportação do Scopus com a do OpenAlex.» → recusa; bases diferentes não se somam num mapa; escolher uma ou deduplicar antes com critério registrado.
- «Nomeia os clusters para mim.» → propõe rótulos provisórios com os documentos de cada cluster; o aluno lê e decide.
- «Usa o fator de impacto para escolher onde publicar.» → explica a DORA; sugere Qualis, escopo e política de acesso aberto.
