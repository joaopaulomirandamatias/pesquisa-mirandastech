# Plano — Plugin Pesquisa MirandasTech

_Versão de 08/09/2026. Página original: docs/plano.html. Esta versão implementa a camada gratuita completa; a camada paga (servidor MirandasTech) fica para depois._

MirandasTech · plano para decisão · 08/09/2026
# Plugin Pesquisa MirandasTech

O que o estudante instala no Claude Code, no Claude Desktop e no Codex; o que cada função faz; como o agente Pesquisador conduz uma pesquisa dentro das normas; e o que pode, e o que não pode, ser remunerado e limitado.
Base: os quatro manuais publicados (Metodologia, Uso de IA, Zotero, Gemini Notebook), os três agentes existentes (Metodólogo, Orientador, Bibliotecário), o conector MCP do Zotero e o hub de pesquisa em construção.

## 1. O que a pessoa instala

Um único pacote, distribuído pelo repositório `pesquisa-mirandastech` (o hub aponta para ele), que se apresenta de forma diferente em cada cliente porque cada cliente aceita coisas diferentes.

  
### Claude Code
`/plugin marketplace add joaopaulomirandamatias/pesquisa-mirandastech` e `/plugin install pesquisa@mirandastech`. Entram: 4 agentes, todas as skills, comandos `/pesquisa:…`, o conector Zotero, um hook de início de sessão e os modelos de arquivo. É o cliente completo.
  
### Codex (app e CLI)
O mesmo repositório traz `.codex-plugin/plugin.json` e `skills/`, o formato do plugin oficial do Zotero da OpenAI, mais `AGENTS.md` e prompts. Sem subagentes: os quatro agentes viram skills invocadas por nome, e o Pesquisador vira o prompt principal.
  
### Claude Desktop e outros clientes MCP
Só conectores: o Zotero local e, no plano pago, o servidor MirandasTech. Não há agentes nem skills aqui; o valor é acesso às ferramentas dentro de qualquer conversa.

> **Quem paga o modelo.** O plugin não gasta créditos seus. O estudante usa a própria assinatura do Claude ou do Codex; o que roda no seu servidor (plano pago) é o único custo de infraestrutura da MirandasTech.

## 2. As funções, uma a uma

| Função | O que faz | Onde roda | Camada |
|---|---|---|---|
| Pesquisador (novo) | Coordena: diagnostica onde o aluno está, cria a pasta do projeto, mantém um único PROGRESSO.md, chama o especialista certo em cada fase e só avança com evidência (seção 3). | Agente (Claude) · prompt principal (Codex) | grátis |
| Metodólogo | Pergunta → objetivos → classificação → método → amostra → instrumento → análise → ética → cronograma; projeto NBR 15287:2025; banca simulada. | Agente/skill local | grátis |
| Orientador (uso de IA) | O que pode ser delegado em cada etapa, registro em USO_DE_IA.csv, declaração de uso, triagem assistida com status preliminar. | Agente/skill local | grátis |
| Bibliotecário + conector Zotero | Configuração do Zotero, auditoria da biblioteca (sem DOI, sem PDF, caixa alta, duplicados), referência ABNT gerada pelo Zotero, exportação Better BibTeX. | Agente/skill + MCP local (API do Zotero) | grátis |
| Leitura e síntese (Gemini Notebook) | Prompts de inventário, triagem, fichamento IMRaD, matriz de síntese, banca; conferência da matriz exportada célula a célula. Sem API: a ponte é por arquivo. | Skill local | grátis |
| Scripts | iniciar_projeto, verificar_citacoes, tamanho_amostra, cronograma, auditar_biblioteca, exportar_bbt, backup_zotero. | Local (Python/bash) | grátis |
| Comandos /pesquisa:… | iniciar, status, proxima, auditar, declarar, banca, entregar: atalhos para as fases do Pesquisador. | Claude Code (Codex: prompts) | grátis |
| Servidor MirandasTech (novo) | Ferramentas que precisam de dados ou processamento que não cabem no computador do aluno: verificação de referências contra a Crossref e as NBR 6023/10520, relatório PRISMA a partir da biblioteca, laudo de conformidade do projeto, rubricas de banca por programa, modelos institucionais, painel de progresso para o professor. | MCP remoto (HTTP, chave por usuário) | pago |

## 3. O Pesquisador: como conduz uma pesquisa dentro das normas

Não é um quinto especialista; é o gerente de projeto. Ele sabe a ordem das fases, quem decide em cada uma (sempre o aluno), qual especialista chamar, qual manual e slide apontar, e qual evidência exige para marcar a fase como concluída. Nunca escreve resultados, nunca inventa dados ou referências, e não libera coleta com pessoas sem parecer do comitê de ética registrado.

- **0 · DIAGNÓSTICO** — Onde o aluno está, prazo, programa, orientador, ferramentas. Cria a pasta e o `PROGRESSO.md`. _(Pesquisador)_

- **1 · PERGUNTA** — Tema → problema → pergunta com «tabela vazia do resultado» → objetivos. _(Metodólogo)_

- **2 · MÉTODO** — Classificação, desenho, amostra, instrumento, análise; o que a IA pode fazer aqui. _(Metodólogo · Orientador)_

- **3 · PROJETO E ÉTICA** — Projeto NBR 15287; CEP quando houver pessoas. Porta fechada até o parecer. _(Metodólogo)_

- **4 · BUSCA E BIBLIOTECA** — Bases, string, coleção por base e data; auditoria da biblioteca. _(Metodólogo · Bibliotecário)_

- **5 · TRIAGEM** — Deduplicar, triagem assistida com status preliminar, decisão do aluno, números para o PRISMA. _(Orientador · Bibliotecário)_

- **6 · LEITURA E SÍNTESE** — PDFs do Zotero → notebook; fichamento; matriz de síntese conferida célula a célula. _(Leitura (Gemini Notebook))_

- **7 · ANÁLISE** — Coleta e análise conforme o método; a IA só onde foi autorizada e registrada. _(Metodólogo · Orientador)_

- **8 · ESCRITA ABNT** — Estrutura NBR 14724, citações 10520, referências 6023 via Zotero; verificação automática. _(Bibliotecário · scripts)_

- **9 · PRÉ-BANCA** — Cinco objeções mais fortes, perguntas prováveis, respostas com página. _(Metodólogo · Leitura)_

- **10 · ENTREGA** — Declaração de uso de IA, backup, versão congelada da biblioteca, checklist final. _(Orientador · Bibliotecário)_

### Regras que valem em todas as fases

- **Evidência antes de marcar.** Uma fase só fecha com o arquivo existente ou o script passando: `DECISOES.md` com a entrada datada, `verificar_citacoes` sem erro, auditoria da biblioteca sem pendência crítica, `USO_DE_IA.csv` preenchido.

- **O aluno decide; o agente formula.** Alternativas com prós e contras; a escolha vai para `DECISOES.md` com data e justificativa. Nada é registrado sem confirmação.

- **Um estado só.** `PROGRESSO.md` substitui os três checklists atuais (os agentes continuam lendo as seções deles). Toda sessão começa por «onde paramos» e termina por «o próximo passo».

- **Rastro para o orientador humano.** `/pesquisa:status` gera um resumo de uma página: fase, decisões, pendências, uso de IA declarado. É o que o professor lê.

## 4. Remuneração: o que dá para cobrar e como limitar

> **O que não dá.** Não existe cobrança nem limite de uso dentro do sistema de plugins do Claude Code nem do Codex. Agentes, skills e prompts são arquivos de texto instalados no computador do aluno: quem tem o repositório tem o conteúdo, e pode copiar. Colocar «limite no plugin» significa, na prática, colocar limite _no seu servidor_, não no texto.

Por isso o desenho separa o que é grátis e aberto (os manuais e os agentes locais, licença CC BY, o que já é público hoje) do que é pago: serviços que rodam no servidor MirandasTech e só respondem com chave válida. É o único ponto em que dá para medir, limitar e cobrar de verdade.

| Plano | O que inclui | Como se limita |
|---|---|---|
| AbertoR$ 0 | Quatro manuais, quatro agentes, skills, scripts, conector Zotero local, comandos. Tudo o que existe hoje mais o Pesquisador. | Não se limita. É a porta de entrada e a divulgação. |
| Pesquisador Proassinatura mensal ou por semestre | Servidor MirandasTech: verificação completa de referências (Crossref + NBR 6023/10520), relatório PRISMA gerado da biblioteca, laudo de conformidade do projeto (15287/14724), banca simulada com rubricas do programa, modelos institucionais (USP, Unicamp…), histórico do PROGRESSO.md na nuvem, suporte no hub. | Chave por aluno com validade; cota de chamadas por mês por ferramenta; renovação pelo hub. A chave fica no .env do projeto; o servidor recusa sem ela. |
| Turmalicença por professor | Tudo do Pro para N alunos, painel do professor com o status de cada projeto (só o que o aluno autorizar), rubricas próprias da disciplina, material de aula a partir dos manuais. | Chaves emitidas pelo professor; cota por turma; expira no fim do semestre. |

### Onde vender e cobrar

- **Hub de pesquisa** como loja: página do plano, checkout (Stripe ou o próprio Hostinger), emissão da chave, painel «minha chave e meu consumo». O hub já vai existir; a loja é uma seção dele.

- **Diretórios oficiais** (conectores do Claude, plugins do Codex): servem para divulgação e instalação em um clique, não para cobrar; nenhum dos dois tem cobrança embutida para terceiros que eu tenha conseguido confirmar. Marcado como confirmar na seção 7.

- **Repositório privado** como alternativa simples: o pacote Pro num repo privado do GitHub e o aluno pagante entra como colaborador. Funciona, mas não limita uso nem impede cópia; serve só como primeiro degrau.

> **Dados dos alunos.** O servidor Pro deve receber o mínimo: referências, metadados e o `PROGRESSO.md`, nunca PDFs nem dados de participantes. Termos de uso e política de privacidade no hub (LGPD), com o aluno sabendo o que sobe.

## 5. Arquitetura

```
pesquisa-mirandastech (GitHub, público) — implementado nesta versão
├── .claude-plugin/marketplace.json     → marketplace «mirandastech»
├── plugins/pesquisa/                   → o plugin do Claude Code
│   ├── .claude-plugin/plugin.json
│   ├── agents/   pesquisador.md · metodologo.md · orientador.md · bibliotecario.md
│   ├── skills/   (as de hoje + leitura-gemini-notebook + pesquisador)
│   ├── commands/ pesquisa:iniciar … pesquisa:entregar
│   ├── .mcp.json (zotero local · mirandastech-pro remoto, opcional)
│   └── modelos/  DECISOES.md · USO_DE_IA.csv · PROGRESSO.md · AGENTS.md
├── .codex-plugin/plugin.json + skills/ + AGENTS.md + codex/prompts/   → pacote do Codex
├── site/  (catálogo dos manuais, trilha, busca, loja)
└── scripts/ (os de hoje, unificados)

servidor-pro (privado, Railway) — MCP HTTP com autenticação por chave
├── /mcp   ferramentas: verificar_referencias · relatorio_prisma · laudo_projeto ·
│          banca_rubrica · modelos_institucionais · progresso_sync
└── /api   chaves, cotas, consumo (alimenta a loja do hub)
```

Os repositórios dos manuais continuam sendo a fonte de cada agente; o hub os agrega no build (como já faz com os sites). Assim uma correção no manual do Zotero atualiza o plugin sem trabalho duplicado.

## 6. Roadmap e esforço

| Etapa | Entrega | Esforço | Depende de |
|---|---|---|---|
| 1 | Plugin aberto no hub (marketplace único, quatro agentes, comandos, pacote do Codex). Zero conteúdo novo além do Pesquisador. | 1 a 2 dias | Repositório do hub no GitHub |
| 2 | Pesquisador: agente, skill com as 11 fases e portas, PROGRESSO.md único, migração dos três checklists. | 2 a 3 dias | Etapa 1; nome do agente |
| 3 | Teste com dois ou três alunos reais do início ao /pesquisa:status; ajustes. | 2 semanas de uso | Etapa 2 |
| 4 | Servidor Pro: primeiras três ferramentas (verificar referências, relatório PRISMA, laudo do projeto), chaves e cotas. | 1 semana | Decisão de preço e de onde cobrar |
| 5 | Loja no hub, termos e privacidade, plano Turma, painel do professor. | 1 semana | Etapa 4; checkout escolhido |
| 6 | Editor de Manuais (agente interno que reproduz a produção de um manual com capturas reais). | 3 a 4 dias | Só quando houver o próximo manual na fila |

## 7. Decisões suas e pontos a confirmar

- **Nome** do agente coordenador e do plugin («Pesquisador», «Pesquisa MirandasTech» são os provisórios).

- **Fronteira grátis/pago**: a proposta deixa tudo o que já existe aberto e cobra só pelo servidor. A alternativa (fechar os agentes num repo privado) rende menos e desgasta a marca; recomendo não fazer.

- **Preço e ciclo**: mensal, semestral, por turma. Meu palpite para começar: semestral para aluno, licença anual para professor.

- **Codex**: espelho completo ou versão reduzida. Como o Codex não tem subagentes, a versão reduzida (Pesquisador como prompt principal, especialistas como skills) é a única honesta.

- confirmar regras de submissão e de cobrança nos diretórios oficiais de conectores do Claude e de plugins do Codex antes de contar com eles na divulgação.

- confirmar forma de autenticação do MCP remoto que o Claude Desktop e o Codex aceitam hoje (OAuth ou cabeçalho com chave) para o servidor Pro.
