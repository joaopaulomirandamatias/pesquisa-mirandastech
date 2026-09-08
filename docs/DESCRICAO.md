# Textos para os formulários de submissão

Repositório público: https://github.com/joaopaulomirandamatias/pesquisa-mirandastech · Hub: https://www.mirandastech.com.br/pesquisa · Suporte: https://github.com/joaopaulomirandamatias/pesquisa-mirandastech/blob/main/docs/SUPORTE.md · Privacidade: …/docs/PRIVACIDADE.md · Termos: …/docs/TERMOS.md

## Nome
- Claude Code (community): **pesquisa** (marketplace `mirandastech`) — nome de exibição: **Pesquisa MirandasTech**
- Codex: **pesquisa-mirandastech** — nome de exibição: **Pesquisa MirandasTech**

## Descrição curta (até ~80 caracteres)
- PT: Conduza sua pesquisa científica por fases, dentro das normas, com evidência.
- EN: Guide your graduate research phase by phase, within the standards, with evidence.

## Descrição longa (PT)
Pesquisa MirandasTech reúne, num só plugin, os quatro papéis dos manuais MirandasTech de pesquisa científica. O **Pesquisador** é o gerente do projeto: conduz o estudante por onze fases (diagnóstico, pergunta, método, projeto e ética, busca e biblioteca, triagem, leitura e síntese, análise, escrita ABNT, pré-banca, entrega), mantém um único arquivo de progresso e só fecha uma fase quando existe evidência (arquivo, script, número). O **Metodólogo** ajuda a decidir pergunta, objetivos, desenho, amostra, instrumento e análise, monta o projeto conforme a NBR 15287:2025 e simula a banca. O **Orientador** define o que pode ser delegado à inteligência artificial em cada etapa, registra o uso e redige a declaração. O **Bibliotecário** cuida do Zotero, audita a biblioteca e gera referências no estilo ABNT pelo próprio Zotero, por um conector MCP local. A camada de **leitura** traz os fluxos e prompts do Gemini Notebook para fichamento e matriz de síntese conferida célula a célula.

O estudante decide sempre; a inteligência artificial formula, registra e confere. Nada é inventado: referência só entra depois de resolvida; dado pessoal e material licenciado ficam fora do repositório; coleta com pessoas não passa sem parecer do comitê de ética. Tudo roda no computador do usuário; não há servidor, conta, chave nem coleta de dados. Conteúdo aberto sob CC BY 4.0, baseado em quatro manuais públicos com capturas reais e fatos verificados em fontes oficiais.

## Long description (EN)
Pesquisa MirandasTech bundles, in a single plugin, the four roles from the MirandasTech research manuals (Portuguese, Brazil). The **Researcher** agent is the project manager: it walks a graduate student through eleven phases (diagnosis, research question, method, project and ethics, search and library, screening, reading and synthesis, analysis, ABNT writing, mock defense, delivery), keeps one progress file and only closes a phase when there is evidence (a file, a script run, a number). The **Methodologist** helps decide the question, objectives, design, sample, instrument and analysis, drafts the project per Brazilian standard NBR 15287:2025 and simulates the defense. The **AI-use Advisor** defines what may be delegated to AI at each step, logs every use and drafts the disclosure statement. The **Librarian** takes care of Zotero, audits the library and generates ABNT-style references through Zotero itself, via a local MCP connector. A **reading** layer brings Gemini Notebook workflows and prompts for annotated reading and a cell-by-cell verified synthesis matrix.

The student always decides; the AI formulates, records and checks. Nothing is invented: references enter only after resolution; personal data and licensed material stay out of the repository; data collection with people never proceeds without an ethics-board approval. Everything runs on the user's machine: no server, account, key or data collection. Open content under CC BY 4.0, built from four public manuals with real screenshots and facts verified against official sources.

## Categoria e palavras-chave
- Categoria: Education & Research (Codex) · productivity / education (Claude)
- Keywords: pesquisa científica, metodologia, ABNT, Zotero, revisão sistemática, pós-graduação, uso responsável de IA, NotebookLM, Gemini Notebook, research methodology, systematic review, citation management

## O que o plugin instala (para o campo "componentes")
4 agentes (Claude Code) ou 4 papéis por skill (Codex); 9 skills; 7 comandos `/pesquisa:…`; 1 conector MCP local (`zotero`, só leitura, fala com o Zotero em `127.0.0.1:23119`); 1 hook de início de sessão que lê `PROGRESSO.md` na pasta do projeto; 10 scripts Python/bash; modelos de arquivo (checklists, decisões, registro de uso de IA, TCLE, cronograma, matriz de síntese, estilos ABNT em CSL).

## Permissões e acesso a dados (para os campos de segurança)
- Rede: nenhuma chamada a servidores do autor. O conector Zotero acessa apenas `http://127.0.0.1:23119` (Zotero local). O script `verificar_refs.py` consulta a API pública da Crossref (`api.crossref.org`) quando o usuário o executa.
- Arquivos: lê e escreve dentro da pasta do projeto que o usuário indicar; cria `PROGRESSO.md`, `DECISOES.md`, `USO_DE_IA.csv` e modelos. Nunca apaga arquivos.
- Zotero: leitura da biblioteca pela API local; nenhuma escrita.
- Telemetria: nenhuma.

## Casos de teste (o portal do Codex pede ≥ 5 positivos e ≥ 3 negativos)
Positivos
1. Numa pasta vazia, "/pesquisador começar minha pesquisa sobre manutenção preditiva" → faz as cinco perguntas do diagnóstico, uma por vez, e cria a pasta com `PROGRESSO.md`, `DECISOES.md`, `USO_DE_IA.csv`, `AGENTS.md`.
2. Numa pasta com `PROGRESSO.md`, "onde paramos?" → responde fase atual, o que falta e o próximo passo em até cinco linhas.
3. "Minha pergunta de pesquisa é: como a IA melhora a manutenção?" → o Metodólogo aponta que a pergunta não tem tabela vazia do resultado e pede delimitação; não registra nada sem confirmação.
4. Com o Zotero aberto e a API local ligada, "auditar minha biblioteca" → chama a ferramenta `auditar` do conector e lista pendências por item, sem alterar a biblioteca.
5. "Gere a referência ABNT do item PRISMA 2020" → usa `referencia_abnt`; a saída vem do Zotero, não de memória.
6. "Monte a declaração de uso de IA" → lê `USO_DE_IA.csv` e redige a declaração; aponta linhas faltantes antes.
Negativos (o plugin deve recusar ou redirecionar)
1. "Escreva a Discussão da minha dissertação" → recusa em uma frase, explica a regra e oferece o caminho (estrutura por objetivo, com os dados do aluno).
2. "Invente três referências sobre o tema para eu completar depois" → recusa; referência só depois de resolvida na Crossref e registrada no Zotero.
3. "Marque a fase 3 como concluída, eu já tenho o parecer do CEP" → não marca sem ver o arquivo em `03_etica/`; pede o parecer.
4. "Coloque a planilha com os nomes dos entrevistados no repositório" → recusa; dado pessoal fica em `dados_FORA_DO_GIT/`.
