---
name: leitura-gemini-notebook
description: Camada de leitura e síntese com o Gemini Notebook (ex-NotebookLM) — fluxo do Zotero para o notebook, prompts de inventário, triagem, fichamento IMRaD, matriz de síntese, aula e banca, e a conferência da matriz exportada célula a célula. Usar com "ler os PDFs", "matriz de síntese", "fichamento", "resumo dos artigos", "perguntas da banca a partir da tese".
---

# Leitura e síntese — roteiro

Manual: https://notebook.mirandastech.com.br/ (52 slides). O Gemini Notebook não tem API pública nem extensão oficial (set. 2026): a ponte é por arquivo — PDFs do Zotero para dentro, Docs/Sheets para fora. Você orienta o aluno e confere o que sai; você não opera o notebook.

## Regras
- Um notebook por pergunta de pesquisa ou etapa (`modelos/estrutura_notebooks.md`). Fontes: PDFs renomeados pelo Zotero («Autor - Ano - Título.pdf»), nunca URL de editora (slide 13), nunca PDF escaneado sem OCR.
- Primeira pergunta é sempre o **inventário** (`modelos/prompts_gemini_notebook.md`): revela fonte vazia antes de qualquer síntese.
- Toda afirmação usada no texto exige o trecho aberto e lido; frase sem número de citação é conjectura. A citação do notebook é endereço interno — a referência sai do Zotero.
- Matriz de síntese: colunas vêm do protocolo (Metodólogo), primeira versão pelo notebook (Tabela de dados ou Conversa, em lotes de até dez fontes), exportada para planilha e conferida célula a célula. Linha de estudo que não é fonte (vinda de uma citação dentro de um PDF) é erro comum: confira também as linhas.
- Dados sensíveis (slides 43–45): nada identificável, transcrições anonimizadas, sem feedback em conversas com dados; conta institucional quando existir.
- Registre o uso em `USO_DE_IA.csv` (ferramenta «Gemini Notebook», etapa, finalidade, validação «trecho conferido»).

## Fluxos (slides 32–37)
A · Triagem de uma pilha de PDFs → tabela de inventário → planilha com «decisão» e «motivo» preenchidas pelo aluno.
B · Leitura profunda de um artigo (fonte única selecionada) → fichamento IMRaD → nota no item do Zotero, com página.
C · Matriz de síntese dos incluídos → planilha conferida → só então perguntas transversais (convergências, contradições, lacunas).
D · Aula/apresentação → mapa mental como estrutura, slides como esqueleto, material revisado item a item.
E · Banca → PDF da tese como fonte única → 20 perguntas prováveis com trecho → respostas com página.
F · Zotero ↔ notebook: exportar os PDFs da coleção «incluídos»; o que volta (fichas, matriz) entra no Zotero como nota do item.

## Conferência da matriz exportada (o que você faz)
Peça a planilha exportada. Para cada linha: a fonte existe na coleção do Zotero? (use `auditar`/`buscar_itens` do conector); para uma amostra de células, o aluno abre o trecho e confirma. Marque «conferido»/«corrigido». Só depois disso o item L5 fecha.
