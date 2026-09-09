# Testes dos agentes (`claude plugin eval`)

Cada pasta é um caso: `case.yaml` (prompt, ferramentas permitidas, graders) e `setup.sh`, que prepara na pasta de trabalho um projeto criado pelo `iniciar_projeto.py` num cenário (`_lib/projeto.sh`: `fase0`, `fase1-aberta`, `fase3`, `material-posterior`). Os graders são de três tipos: `regex` (a resposta cita a fase certa, não marca no arquivo), `tool_used` (o agente não chamou Edit/Write) e `llm` (um juiz lê a resposta contra critérios escritos).

| Caso | O que protege |
|---|---|
| `onde-paramos-fase0` | estado inicial correto; pergunta do diagnóstico; nada marcado |
| `onde-paramos-fase3` | lê fases fechadas e decisões; aponta a porta da fase 3 |
| `nao-fecha-sem-evidencia` | recusa marcar fase sem evidência escrita |
| `material-posterior` | registra material da fase 6, mas fecha as anteriores primeiro |
| `metodologo-pergunta-ampla` | critica pergunta que pressupõe resultado; tabela vazia |
| `orientador-triagem` | status preliminar, decisão humana, `USO_DE_IA.csv` |
| `bibliotecario-api-local` | orienta a API local sem inventar coleções |
| `sem-projeto` | sem `PROGRESSO.md`, não inventa estado |
| `status-relatorio` | `/pesquisa:status` roda o `relatorio_orientador.py`, grava o relatório e comenta sem marcar (exige Bash funcionando no sandbox) |

Rodar (o `eval` está em acesso antecipado no Claude Code; o `setup.sh` só roda com `--scaffold`):

```bash
CLAUDE_CODE_WALNUT_SPIRE=1 claude plugin eval . --scaffold --ablation none --allow-tools Edit Write Bash \
  --runs 1 --judge-model claude-sonnet-5 --no-publish --report evals/results/relatorio.html
# só alguns casos:
CLAUDE_CODE_WALNUT_SPIRE=1 claude plugin eval . --scaffold --ablation none --allow-tools Edit Write Bash --case "onde-paramos-*"
```

Notas de execução (09/09/2026): o Claude Code do terminal precisa estar logado (`claude auth status`); `--ablation none` evita o braço «sem plugin», que dobra o custo; `--judge-model claude-sonnet-5` deixa o juiz menos errático que o padrão (haiku); uma rodada completa com `--runs 1` custou cerca de US$ 3,50 e levou 8 minutos. O CI não roda os evals automaticamente; rode antes de publicar uma versão e guarde o relatório em `evals/results/` (ignorado pelo Git). Primeira rodada completa: 8/8 casos de conversa passando após ajuste dos critérios. O caso `status-relatorio` depende do Bash dentro do sandbox do Claude Code; na máquina do autor o sandbox falha (`apply-seccomp: Permission denied`, namespaces de usuário restritos) e o caso reprova por ambiente, não por comportamento — o agente relata que não conseguiu rodar o script e monta o relatório à mão, sem alterar nada. Rode-o num ambiente onde o sandbox funciona (CI) ou exclua-o com `--case`.
