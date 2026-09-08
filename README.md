# Pesquisa MirandasTech — plugin para Claude Code e Codex

**Hub de pesquisa:** https://www.mirandastech.com.br/pesquisa (todos os manuais, o plugin e as novidades).

Um só pacote com os quatro papéis dos manuais MirandasTech, para conduzir uma pesquisa de pós-graduação dentro das normas, fase a fase, com evidência:

| Papel | O que faz | Manual |
|---|---|---|
| **Pesquisador** (novo) | Gerente do projeto: 11 fases (diagnóstico → pergunta → método → projeto e ética → busca e biblioteca → triagem → leitura e síntese → análise → escrita ABNT → pré-banca → entrega), um único `PROGRESSO.md`, chama o especialista certo, só fecha fase com evidência. O aluno decide sempre. | os quatro |
| **Metodólogo** | Pergunta, objetivos, classificação, desenho, amostra, instrumento, análise, projeto NBR 15287:2025, ABNT, banca simulada | https://metodologia.mirandastech.com.br/ |
| **Orientador** | O que pode ser delegado à IA em cada etapa, registro em `USO_DE_IA.csv`, triagem assistida com status preliminar, declaração de uso | https://manual.mirandastech.com.br/ |
| **Bibliotecário** + conector MCP `zotero` | Zotero: configuração, auditoria da biblioteca, referências ABNT geradas pelo Zotero, exportação Better BibTeX | https://zotero.mirandastech.com.br/ |
| **Leitura** (skill) | Fluxos e prompts do Gemini Notebook; conferência da matriz de síntese célula a célula | https://notebook.mirandastech.com.br/ |

Tudo nesta versão é **gratuito, aberto (CC BY 4.0) e roda no computador do aluno**. Não há servidor, chave nem cota. O plano completo, inclusive a camada paga prevista para depois, está em [`docs/PLANO.md`](docs/PLANO.md).

## Instalar

**Claude Code** (plugin completo: agentes, skills, comandos, conector, hook):
```
/plugin marketplace add joaopaulomirandamatias/pesquisa-mirandastech
/plugin install pesquisa@mirandastech
```
ou `bash scripts/instalar_claude.sh` (também registra o conector Zotero no Claude Desktop, se existir).

**Codex** (app e CLI), como plugin (marketplace próprio, sem depender do diretório da OpenAI):
```
codex plugin marketplace add joaopaulomirandamatias/pesquisa-mirandastech
codex plugin add pesquisa-mirandastech@mirandastech
```
ou `bash scripts/instalar_codex.sh`, que faz isso e ainda registra o conector `zotero` em `~/.codex/config.toml` e instala os prompts `/pesquisador`, `/metodologo`, `/orientador`, `/bibliotecario`. Na pasta do projeto o Codex lê `AGENTS.md`.

Requisitos: Python 3, Git, `uv` (para o conector Zotero; alternativa: `pip install mcp`), Zotero 7+ aberto com a API local ligada (Configurações → Avançado) para as ferramentas de biblioteca.

## Usar

```bash
python3 scripts/iniciar_projeto.py minha-pesquisa --tema "…" --metodo "revisão sistemática" --programa "PPGEE" --prazo 2027-03
cd minha-pesquisa
```
No Claude Code: **«Pesquisador, onde paramos?»** ou os comandos `/pesquisa:iniciar`, `/pesquisa:status`, `/pesquisa:proxima`, `/pesquisa:auditar`, `/pesquisa:declarar`, `/pesquisa:banca`, `/pesquisa:entregar`. No Codex: `/pesquisador onde paramos`.

O projeto criado tem: pastas por etapa, `PROGRESSO.md` (fases + checklists Método, Uso de IA, Biblioteca e Leitura, com os slides de cada item), `DECISOES.md`, `USO_DE_IA.csv`, `AGENTS.md` (regras lidas por qualquer agente), `ACORDO_ORIENTADOR.md`, protocolo, modelos de matriz de síntese, buscas, tabela de operacionalização, livro de códigos, cronograma, TCLE, estrutura de coleções do Zotero e prompts do Gemini Notebook. Pastas de um projeto antigo dos manuais (com `PROGRESSO_IA.md` ou `PROGRESSO_METODOLOGIA.md`) são migradas sem sobrescrever nada.

## O que há no repositório

| Onde | O que |
|---|---|
| `.claude-plugin/` | manifesto do plugin `pesquisa` e marketplace `mirandastech` (lista também o plugin só-Zotero) |
| `agents/` | `pesquisador.md`, `metodologo.md`, `orientador.md`, `bibliotecario.md` |
| `skills/` | `pesquisador`, `metodologo-pesquisa`, `projeto-nbr15287`, `abnt-citacoes-referencias`, `banca-simulada`, `orientador-ia-pesquisa`, `triagem-assistida`, `bibliotecario-zotero`, `leitura-gemini-notebook` |
| `commands/` | os sete comandos `/pesquisa:…` |
| `.mcp.json` · `scripts/zotero_mcp.py` | conector MCP da biblioteca Zotero (7 ferramentas, só leitura) |
| `hooks/hooks.json` | ao abrir uma sessão numa pasta com `PROGRESSO.md`, mostra as pendências e lembra de chamar o Pesquisador |
| `scripts/` | `iniciar_projeto.py`, `verificar_citacoes.py`, `verificar_refs.py`, `tamanho_amostra.py`, `cronograma.py`, `auditar_biblioteca.py`, `exportar_bbt.sh`, `backup_zotero.sh`, `instalar_claude.sh`, `instalar_codex.sh` |
| `modelos/` | arquivos copiados para o projeto; estilos ABNT (.csl); prompts do Gemini Notebook |
| `.codex-plugin/` · `.agents/plugins/marketplace.json` · `AGENTS.md` · `codex/prompts/` | pacote do Codex (manifesto do plugin, marketplace, instruções e prompts) |
| `docs/` | o plano (Markdown e HTML) |
| `.github/workflows/verificar.yml` | CI: manifestos, frontmatter de agentes/skills/comandos, scripts |

## Como citar
MATIAS, J. P. M. *Pesquisa MirandasTech: plugin de acompanhamento de pesquisa para Claude Code e Codex.* v1.0, set. 2026. CC BY 4.0.

## Declaração de uso de IA
Construído com assistência de IA (Claude, Anthropic) a partir dos quatro manuais MirandasTech. O autor responde pelo conteúdo. Os manuais de origem e suas verificações de fatos estão nos repositórios `metodologia-pesquisa-cientifica`, `ia-na-pesquisa-cientifica`, `zotero-pesquisa-cientifica` e `gemini-notebook-pesquisa-cientifica`.
