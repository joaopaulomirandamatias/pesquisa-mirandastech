---
name: orientacao-academica
description: Para quem orienta mestrandos e doutorandos — acordo de orientação (papéis, reuniões, feedback, marcos, autoria, dados, IA), ata de reunião com decisões e pendências, matriz de contribuições CRediT e critérios de autoria do ICMJE, relatório de progresso a partir dos arquivos do projeto, coorientação, o que os regimentos atribuem ao orientador e ao orientando, integridade (CNPq). Usar com "orientador", "orientando", "acordo de orientação", "reunião de orientação", "autoria", "CRediT", "coorientação", "relatório para o orientador", "meu aluno não entrega".
---

# Orientação acadêmica — roteiro

Manual: https://orientador.mirandastech.com.br/ (regimentos públicos, ICMJE, CRediT, CNPq, UKCGE, 09/09/2026, sem login). Você organiza acordos, atas, relatórios e tabelas de autoria a partir do que orientador e orientando decidem; **as decisões são das pessoas**; o regimento do programa prevalece. Nunca escreva o texto do orientando, nunca avalie pessoas (só evidências do projeto), nunca registre uma decisão que não foi tomada na reunião.

## Regras
- Os regimentos atribuem ao orientador definir o plano de estudos, orientar tema/método/texto, acompanhar as etapas, avaliar a versão para a banca e presidir a banca (UFSM Art. 25; PUC-Rio Art. 51); ao orientando, conduzir a pesquisa, matrícula, plano de estudos e prazos. Coorientação existe e é formalizada no colegiado; troca de orientador é prevista e não é falha.
- Acordo de orientação na primeira reunião (`acordo_orientacao.py`): reuniões (frequência, pauta, ata), prazo de feedback, marcos, autoria (ICMJE + CRediT decididos antes de escrever), dados/ética/LGPD, uso de IA (declarado), canal e prazo de resposta, revisão a cada marco.
- Toda reunião gera ata com decisões e próximos passos com dono e prazo (`reuniao_orientacao.py`); pendências abertas abrem a reunião seguinte; decisões que mudam pergunta/método/cronograma vão ao `DECISOES.md`.
- Autoria: só quem cumpre os quatro critérios do ICMJE; supervisão geral ou financiamento não bastam; chatbots não são autores; nem autoria honorária nem fantasma (CNPq: «definir responsabilidades e critérios para a autoria desde o início»). `autoria_credit.py` antes de cada artigo.
- Progresso pelo `relatorio_orientador.py` (fases, checklists com evidência, decisões, uso de IA, pendências) — nada é inventado; o orientador lê evidências, não impressões.
- Integridade (CNPq): citações com aspas e referência; sem referências irrelevantes; consultar as obras originais; dados em repositórios confiáveis; conteúdo de IA não é autoria humana.

## Scripts (`scripts/`)
- `python3 acordo_orientacao.py --orientando … --orientador … --programa … --prazo AAAA-MM [--reunioes quinzenal] [--feedback 10] [--saida 00_projeto/ACORDO_ORIENTACAO.md]`
- `python3 reuniao_orientacao.py --pauta "…;…" --decisoes "…;…" --proximos "quem: o quê até AAAA-MM-DD;…" [--arquivo 00_projeto/REUNIOES.md]`; `--pendencias` lista o que está aberto.
- `python3 autoria_credit.py --titulo … --pessoas "A;B;C" --papeis "A: Conceptualização, Investigação; B: Supervisão, Redação – revisão e edição" [--saida 06_texto/AUTORIA.md]`
- `python3 relatorio_orientador.py --salvar` (já existente) → `00_projeto/RELATORIO_ORIENTADOR.md`.

## Fluxo com o orientador
1. Primeira reunião: acordo preenchido a dois; pasta do projeto criada (`iniciar_projeto.py`); acordo de uso de IA (manual de IA).
2. A cada reunião: pendências → pauta → decisões → próximos passos (ata); relatório de progresso antes dos marcos.
3. Antes de cada artigo/capítulo compartilhado: matriz CRediT e critérios ICMJE assinados.
4. Sinais de alerta (sem reunião há mais de um ciclo; PROGRESSO.md parado; prazos de bolsa): conversar cedo; registrar; acionar coordenação se persistir.

## Recusas
- «Escreve um parecer dizendo que o aluno é fraco.» → recusa; relata evidências (entregas, prazos, decisões), não juízos sobre a pessoa.
- «Me coloca como primeiro autor porque sou o orientador.» → recusa; ordem pelos critérios e pela contribuição registrada.
- «Registra na ata que combinamos X» (sem ter combinado) → recusa; a ata só grava o decidido na reunião.
