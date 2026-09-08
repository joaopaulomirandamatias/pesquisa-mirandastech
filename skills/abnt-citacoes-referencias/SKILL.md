---
name: abnt-citacoes-referencias
description: Confere citações e lista de referências de um texto acadêmico conforme ABNT NBR 10520:2023 e NBR 6023:2025 — autor-data sem caixa alta, página em citação direta, et al., consistência texto ↔ lista — usando scripts/verificar_citacoes.py. Usar em "confere minhas citações", "revisa a ABNT", "referências estão certas?".
---

# Citações e referências — NBR 10520:2023 · NBR 6023:2025

1. Rode `python3 scripts/verificar_citacoes.py <arquivo.md|.txt|.tex>`; ele lista: citações autor-data em caixa alta (formato de 2002), citações diretas sem página, autores citados sem entrada na lista, entradas da lista não citadas, DOIs no formato inválido.
2. Para cada aviso, mostre a linha e a forma correta:
   - `(GIL, 2017)` → `(Gil, 2017)`; `(MARCONI; LAKATOS, 2017)` → `(Marconi; Lakatos, 2017)`.
   - Citação direta curta: aspas + `(Autor, ano, p. N)`; longa: recuo 4 cm, fonte menor, sem aspas, com página.
   - Quatro ou mais autores: `(Page et al., 2021)` de modo uniforme no documento.
   - `apud` só quando o original é inacessível.
3. Referências (6023:2025): ordem alfabética, destaque uniforme do título, DOI sempre que existir, «Disponível em / Acesso em» para o que só existe on-line; para mídias sociais, podcasts e vídeos siga os exemplos novos da norma (tutorial da biblioteca).
4. Resolva cada DOI na Crossref (`scripts/verificar_refs.py` do repositório de IA) antes de dar a lista por conferida.
5. Nunca reescreva a lista à mão: corrija no gerenciador (Zotero) e regenere.
