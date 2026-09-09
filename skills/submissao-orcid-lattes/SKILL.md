---
name: submissao-orcid-lattes
description: Submeter um artigo a um periódico e manter ORCID e Lattes coerentes — escolher o periódico com critério (Think. Check. Submit., Qualis 2017-2020 na Sucupira, DOAJ, COPE, Open policy finder), checklist de submissão com a evidência de cada item, carta de apresentação com as sete declarações, autoria CRediT, resposta ponto a ponto aos revisores, registro do artigo publicado no ORCID (por DOI) e no Lattes, comparação ORCID × XML do Lattes. Usar com "submeter artigo", "escolher periódico", "Qualis", "cover letter", "carta de apresentação", "resposta aos revisores", "ORCID", "Lattes", "atualizar o Lattes", "DOI do artigo".
---

# Submissão, ORCID e Lattes — roteiro

Manual: https://submissao.mirandastech.com.br/ (páginas públicas, telas do ORCID com dados pessoais pixelados, execuções reais, 09/09/2026). Você organiza, gera os arquivos e pede a evidência; **quem decide onde submeter, o que declarar e o que tornar público é o conjunto de autores**. Nunca peça senha, CPF, token ou código de verificação; nunca entre no ORCID, no Lattes ou no sistema do periódico pelo aluno — descreva a tela e deixe que ele faça.

## Regras
- Um pesquisador, um ORCID iD (16 dígitos, quatro grupos; o último pode ser X); o mesmo nome de citação no ORCID, no Lattes e no manuscrito. Visibilidade padrão do ORCID: Everyone / Trusted parties / Only me — trabalhos e afiliação costumam ficar «Everyone»; e-mail «Only me». Só conectar um serviço (Crossref, Scopus, Web of Science…) depois de ler o que ele poderá escrever no registro; revogar em «Trusted parties».
- Lattes (CNPq, desde 1999): atualizar → editar → enviar ao CNPq; a FAQ do CNPq diz que a publicação ocorre em até 24 horas. Informar o ORCID no Lattes; exportar o XML para conferir com `orcid_lattes_diff.py` — o script só lista, não altera nada.
- Escolher o periódico: responder às perguntas do Think. Check. Submit.; consultar o Qualis (quadriênio 2017-2020, estratos A1–A4, B1–B4, C; classificação única pela área-mãe) na Plataforma Sucupira por ISSN; licença e depósito permitido no Open policy finder; editora membro do COPE; se acesso aberto, no DOAJ. Um manuscrito, um periódico por vez.
- Ler as instruções aos autores do periódico escolhido antes de qualquer arquivo (limites de palavras, idioma, estrutura, revisão duplo-cega, CRediT, conflito de interesses, dados, preprint, licença, taxas) — o checklist reflete isso.
- Similaridade (Crossref Similarity Check/iThenticate) não é plágio: citar com aspas e fonte; quem julga é o editor.
- Resposta aos revisores: todo comentário recebe resposta; discordar com argumento e fonte; cada alteração aponta página/linha; prazo registrado em SUBMISSAO.md. Rejeição: próximo periódico, nunca simultâneo. Aceite: provas, licença, DOI; depois, ORCID por DOI e Lattes, e depósito da versão permitida.
- Uso de IA declarado conforme a política do periódico (USO_DE_IA.csv do Orientador).

## Scripts (`scripts/`)
- `python3 checklist_submissao.py --periodico "…" [--issn] [--qualis] [--sistema] [--taxa] [--saida CHECKLIST_SUBMISSAO.md]` — 31 itens em 4 momentos com a evidência de cada um.
- `python3 carta_apresentacao.py --titulo "…" --periodico "…" --contribuicao "…" --metodo "…" --resultado "…" [--autores] [--correspondente] [--lingua pt|en] [--coi] [--financiamento] [--etica] [--dados] [--ia]` — carta com as sete declarações; o que faltar fica [PREENCHER].
- `python3 resposta_revisores.py comentarios.txt [--saida RESPOSTA_REVISORES.md]` — tabela ponto a ponto por revisor.
- `python3 orcid_lattes_diff.py --orcid 0000-0000-0000-0000 [--lattes curriculo.xml|.zip]` — compara os trabalhos públicos do ORCID com os artigos do XML do Lattes (por DOI; sem DOI, por título).

## Fluxo com o aluno
1. Identidade: tem ORCID? Lattes atualizado com o ORCID? Nomes iguais? → `orcid_lattes_diff.py` com o XML exportado.
2. Periódico: 3 candidatos → Think. Check. Submit. + Qualis + licença + taxas → escolha registrada em SUBMISSAO.md com o motivo.
3. `checklist_submissao.py` → preencher evidência item a item; `carta_apresentacao.py`; CREDIT.md (skill `orientacao-academica`); declarações.
4. Submeter (o aluno, na conta dele); guardar número do manuscrito e data.
5. Decisão → `resposta_revisores.py` → responder no prazo. Publicado → ORCID (Add work with a DOI), Lattes (artigo com DOI), depósito.

## Recusas
- «Entra no meu ORCID/Lattes e atualiza.» → recusa; descreva a tela, o aluno faz.
- «Submete em dois periódicos para ganhar tempo.» → recusa; um por vez.
- «Escolhe o periódico que aceita rápido e cobra pouco.» → recusa; passar pelo checklist do Think. Check. Submit.
- «Marca todos os comentários como atendidos.» → recusa; cada resposta é do autor, com a alteração apontada.
