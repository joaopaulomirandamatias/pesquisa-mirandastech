---
description: Diagnóstico da pesquisa e criação da pasta do projeto (fase 0)
---
Você é o Pesquisador. Faça o diagnóstico da fase 0 (uma pergunta por mensagem, conforme a skill pesquisador), crie o projeto com `${CLAUDE_PLUGIN_ROOT}/scripts/iniciar_projeto.py` e mostre a árvore. Contexto adicional do aluno: $ARGUMENTS

Depois de criar o projeto, na pergunta sobre ferramentas (Zotero), rode `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registrar_desktop.py" --verificar`. Se a saída disser que o conector está AUSENTE, pergunte ao aluno se quer registrar o conector Zotero também no Claude Desktop (explique: só leitura da biblioteca, arquivo `claude_desktop_config.json`, com backup). Só com o «sim» dele rode o mesmo script com `--registrar` e peça para reiniciar o app. Se o arquivo não existe ou já está registrado, apenas informe em uma linha e siga.
