---
name: busca-bases-abertas
description: Monta e executa buscas reprodutíveis em bases científicas — Portal CAPES sem login, Google Acadêmico, IEEE Xplore, Semantic Scholar, PubMed/LILACS, arXiv, SciELO, BDTD/oasisbr, BASE, DOAJ — e por API (OpenAlex, Crossref, Unpaywall, PubMed, arXiv), com diário de busca no padrão PRISMA-S. Usar com "buscar artigos", "string de busca", "quais bases", "OpenAlex", "exportar para o Zotero", "PDF aberto", "Qualis", "periódico predatório".
---

# Busca em bases científicas — roteiro

Manual: https://busca.mirandastech.com.br/ (capturas reais de 09/09/2026). Você monta a estratégia, roda os scripts e registra; **o aluno escolhe as bases e aprova a string**. Nunca faça login em proxy, CAFe ou base por assinatura; nunca peça senha; nunca cite Sci-Hub ou similares.

## Regras
- Mais de uma base sempre (Bramer et al., 2016; 2017). Google Acadêmico só como complemento (não reprodutível; 1.000 resultados; bloqueia robôs).
- Construir a string por conceitos (Bramer; De Jonge; Rethlefsen, 2018): termos livres + vocabulário controlado por conceito; OR dentro, AND entre; traduzir a sintaxe para cada base (tabela no manual).
- Registrar em `01_buscas/BUSCA.md`: base e plataforma, data, consulta exata, filtros, total, arquivo exportado (com hash), revisão por pares da estratégia (PRESS). É o que o PRISMA-S pede (Rethlefsen et al., 2021).
- Preferir bases abertas com API para reprodutibilidade: OpenAlex (chave gratuita opcional; `mailto=`), Crossref (`mailto=` no polite pool), Unpaywall (`email=` obrigatório), PubMed E-utilities (3 req/s), arXiv (1 chamada a cada 3 s), DOAJ (2 req/s). Semantic Scholar sem chave devolve 429 com frequência: peça a chave.

## Scripts (só biblioteca padrão; rodar de `01_buscas/`)
- `scripts/buscar_openalex.py '<consulta>' --campo title_and_abstract --desde AAAA --tipos article,book-chapter,preprint --email seu@email.br` → `busca_openalex.csv` (title, abstract, year, doi, authors, source, is_oa, type, openalex_id), `busca_openalex.ris` (importar no Zotero) e `diario_busca_<data>.json` (consulta, filtros, data, total). Use `--campo search` para busca com stemming em texto completo.
- `scripts/contar_bases.py '<consulta>' --email seu@email.br` → tabela com o total em OpenAlex, Crossref, PubMed, arXiv, DOAJ e Semantic Scholar na mesma data (os totais diferem: cobertura e sintaxe variam — registre todos).
- `scripts/verificar_oa.py entrada.csv saida.csv --email seu@email.br` → acrescenta `is_oa`, `oa_status`, `pdf_url` pelo Unpaywall.

## Fluxo com o aluno
1. Pergunta e conceitos (Metodólogo) → lista de termos por conceito, em português e inglês.
2. Escolha das bases pelo tipo de literatura (tabela «qual base para quê» do manual): engenharia → IEEE Xplore, OpenAlex, Scopus/WoS pelo CAFe; saúde → PubMed, LILACS; teses → BDTD/oasisbr/Catálogo CAPES; repositórios → BASE, CORE; periódicos abertos → DOAJ, SciELO.
3. Contar antes de baixar (`contar_bases.py`; `group_by` do OpenAlex); ajustar a string até o total ser triável.
4. Baixar (`buscar_openalex.py`; exportação RIS/BibTeX/.nbib das outras bases) → importar no Zotero (Bibliotecário) → deduplicar → triagem (skill `revisao-sistematica-prisma`).
5. Verificar acesso aberto (`verificar_oa.py`; extensão Unpaywall; «Encontrar PDF disponível» no Zotero); o que for fechado, pelo CAFe ou pedindo ao autor.
6. Avaliar periódicos suspeitos: Qualis (Sucupira), SJR, DOAJ, Think. Check. Submit.; verificar retratações (`is_retracted`, Retraction Watch).
7. Fechar a fase 4 no `PROGRESSO.md` com o diário preenchido, arquivos e hashes.

## Recusas
- «Entra no Portal CAPES com meu login.» → recusa; explica o caminho e o aluno entra.
- «Pega o PDF de qualquer jeito.» → recusa; Unpaywall, repositório, CAFe ou pedido ao autor.
- «Inventa uma referência que sustente isso.» → recusa; busca na base e resolve o DOI.
- «Diz que buscou no Scopus.» → recusa; só registra buscas realmente executadas, com data e total.
