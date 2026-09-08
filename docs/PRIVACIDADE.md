# Política de privacidade — Pesquisa MirandasTech
_Versão 1.0, 8 de setembro de 2026. Vale para o plugin «Pesquisa MirandasTech» (Claude Code e Codex), seus scripts, o conector MCP «zotero» e os manuais publicados em mirandastech.com.br._

## Quem é o responsável
MirandasTech, de João Paulo Miranda Matias (Brasil). Contato: contato@mirandastech.com.br. Para os fins da Lei Geral de Proteção de Dados (Lei 13.709/2018, LGPD), a MirandasTech é a controladora apenas dos dados descritos na seção «O que coletamos»; do que o usuário produz com o plugin, o próprio usuário é o controlador.

## O que o plugin faz com os seus dados
- **Roda no seu computador.** Agentes, skills, comandos, scripts e o conector são arquivos instalados localmente. Não existe servidor da MirandasTech, conta, chave, cadastro ou telemetria. Nada do que você escreve, dos seus arquivos ou da sua biblioteca é enviado à MirandasTech.
- **O conector Zotero** lê a sua biblioteca pela API local do Zotero (`http://127.0.0.1:23119`), apenas quando você o usa, e não escreve nem envia nada para fora do seu computador.
- **O script `verificar_refs.py`**, quando você o executa, consulta a API pública da Crossref (api.crossref.org) enviando apenas DOIs ou títulos de referências. A Crossref tem política própria de privacidade.
- **Arquivos criados** (`PROGRESSO.md`, `DECISOES.md`, `USO_DE_IA.csv`, modelos) ficam na pasta do seu projeto, sob o seu controle. O plugin recomenda, e o `.gitignore` gerado reflete, manter dados pessoais e material licenciado fora do controle de versão (`dados_FORA_DO_GIT/`).

## O que coletamos
Nada por meio do plugin. A distribuição é feita pelo GitHub, que registra acessos conforme a política do GitHub. Se você nos escrever por e-mail ou abrir uma issue, guardamos a mensagem para responder.

## O que os provedores de IA recebem
O plugin é executado dentro do Claude Code (Anthropic) ou do Codex (OpenAI). Tudo o que você escreve nessas ferramentas, inclusive o conteúdo de arquivos que os agentes leem, é processado por esses provedores sob os termos e a política de privacidade **deles**, não da MirandasTech. Verifique as configurações de retenção e treinamento da sua conta. O plugin não altera essas configurações.

## Dados sensíveis e de pesquisa
O plugin foi desenhado para não precisar de dados pessoais de participantes: as regras dos agentes proíbem copiar dados identificáveis, transcrições não anonimizadas ou material licenciado para o repositório, e nenhuma coleta com pessoas é liberada sem parecer do comitê de ética. Ainda assim, a decisão de enviar qualquer conteúdo a um provedor de IA é sua e deve seguir o termo de consentimento e o comitê de ética do seu projeto. Os manuais orientam a usar contas institucionais quando existirem.

## Seus direitos
Como não mantemos dados seus, não há o que acessar, corrigir ou excluir do nosso lado. Para os dados processados pela Anthropic, pela OpenAI, pelo GitHub ou pela Crossref, exerça os direitos junto a eles. Dúvidas: contato@mirandastech.com.br.

## Mudanças
Alterações nesta política são publicadas no repositório, com data e versão. O uso continuado após a publicação significa ciência da nova versão.
