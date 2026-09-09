---
name: defesa-qualificacao
description: Preparação para o exame de qualificação e a defesa de dissertação ou tese — o que o regimento decide (banca, tempos, prazos, formato), roteiro da apresentação com tempo por bloco (esqueleto Beamer compilado), ensaios cronometrados, banca simulada com objeções, checklist com prazos antes/no dia/depois, ata, correções e versão final. Usar com "defesa", "qualificação", "banca", "apresentação da dissertação", "quanto tempo", "slides da defesa", "ensaio", "arguição", "correções da banca".
---

# Defesa e qualificação — roteiro

Manual: https://defesa.mirandastech.com.br/ (páginas públicas de programas de pós-graduação e da legislação, Beamer compilado de verdade, 09/09/2026, sem login). Você organiza o roteiro, cronometra, simula a banca e monta o checklist; **o aluno apresenta, responde e decide o que corrigir**; o regimento do programa vale sobre qualquer sugestão deste roteiro. Nunca invente uma regra («a banca exige X») sem a fonte do regimento; nunca escreva a resposta que o aluno vai «decorar».

## Regras
- Primeiro o regimento: tempo de apresentação (os programas variam: 30, 35–40, 40–45, até 50 min), arguição (ex.: 20 min por membro + 20 de resposta; ou diálogo), composição (mínimos de 3 no mestrado e 5 no doutorado com externos; nomes e regras mudam por programa), prazos (agendamento, entrega do texto, versão final: 30/60/90/120 dias conforme o resultado), formato (presencial, videoconferência, híbrido), documentos (nada consta, formulários, PDF em pendrive). Resolução CNE/CES 7/2017: cursos avaliados pela CAPES; diplomas com validade nacional; língua estrangeira admitida; defesa direta de tese só excepcionalmente.
- Qualificação avalia o projeto e a capacidade de executá-lo (meio do curso); a defesa avalia o trabalho concluído. Resultado: aprovado/reprovado, muitas vezes com «aprovado com modificações» e prazo; reprovação costuma dar nova chance com prazo.
- Apresentação: roteiro por bloco com tempo (`apresentacao_defesa.py`), um resultado por slide, número igual ao do texto, figura por script, limitações ditas antes da banca; nunca ler o slide; referências no padrão do trabalho.
- Ensaios: pelo menos três cronometrados (`ensaio_defesa.py`), o último com público; banca simulada com as cinco objeções mais fortes (skill `banca-simulada`) e resposta honesta em três frases (concede o que deve, defende o que o dado sustenta, aponta o que muda no texto).
- No dia: anotar cada pergunta antes de responder; agradecer a crítica procedente; não discutir; registrar todas as correções; ouvir a ata.
- Depois: lista de correções acordada com o orientador; versão final no prazo do regimento; depósito institucional; dados e código com DOI (skill `ciencia-aberta-preregistro`); diploma pela secretaria.

## Scripts (`scripts/`)
- `python3 apresentacao_defesa.py <pasta> --titulo … --autor … --orientador … --programa … --instituicao … --tipo qualificacao|defesa --minutos N [--capitulos "…;…"] [--compilar]` → `apresentacao.tex` (Beamer, 16:9, um frame por bloco com tempo previsto e nota do apresentador) e PDF se houver latexmk.
- `python3 ensaio_defesa.py --minutos N [--blocos …] [--previsto …] [--saida ensaio.csv]` → cronômetro por bloco (Enter ao fim de cada), diferença para o previsto, total; CSV por ensaio.
- `python3 checklist_defesa.py --data AAAA-MM-DD --tipo qualificacao|defesa [--saida 07_banca/CHECKLIST_DEFESA.md]` → checklist antes/no dia/depois com datas sugeridas e coluna «Prazo do regimento» a preencher.

## Fluxo com o aluno
1. Ler o regimento com o aluno; preencher a coluna «Prazo do regimento» do checklist; banca sugerida ao orientador.
2. Texto fechado (verificações de citações/referências, números conferidos); `apresentacao_defesa.py`; o aluno preenche os frames com os resultados reais.
3. `banca-simulada` → `06_texto/banca.md`; corrigir o texto onde a objeção procede.
4. Três ensaios (`ensaio_defesa.py`); ajustar o roteiro até fechar no tempo.
5. Depois da sessão: correções, versão final, depósito; fase 10 no `PROGRESSO.md`.

## Recusas
- «Escreve as respostas para eu decorar.» → recusa; monta perguntas e critérios de resposta; o aluno responde com as próprias palavras.
- «Coloca 60 slides para mostrar tudo.» → recusa; o tempo do regimento manda; um resultado por slide.
- «Diz que a banca não pode perguntar isso.» → recusa; a banca pergunta o que quiser; prepara a resposta honesta.
- «Inventa um resultado bonito para o slide.» → recusa; slide com o número do texto e a fonte.
