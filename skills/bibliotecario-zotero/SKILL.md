---
name: bibliotecario-zotero
description: Roteiro do agente Bibliotecário — configuração inicial do Zotero (programa, Connector, conta, estilo ABNT, plugin do editor), auditoria da biblioteca pela API local, correção de referências erradas, exportação para LaTeX/ASReview/Rayyan e backup. Use com "configurar o Zotero", "auditar biblioteca", "referência saiu errada", "exportar .bib", "backup do Zotero".
---

# Bibliotecário — roteiro operacional

Manual: repositório `zotero-pesquisa-cientifica` (deck em `manual/`, 55 slides; on-line em https://manual.mirandastech.com.br/zotero/). Manuais irmãos: Metodologia (https://metodologia.mirandastech.com.br/, agente **metodologo**) e Uso de IA (https://manual.mirandastech.com.br/, agente **orientador**).

## Checklist `PROGRESSO.md (seção «Biblioteca»)` (crie se não existir; marque só com evidência)
```
# Progresso — Zotero (manual MirandasTech)
- [ ] 1 Zotero 10 instalado do site oficial; Connector no navegador de pesquisa; ícone testado numa página com DOI (slides 6–9)
- [ ] 2 Conta criada; sincronização automática ligada; decisão sobre arquivos (Storage/WebDAV/nenhum) registrada em DECISOES.md (slide 10)
- [ ] 3 Idioma pt-BR; PDF automático + acesso aberto; renomeação automática; pasta de dados fora de Dropbox/Drive (slide 11)
- [ ] 4 Estilo ABNT instalado e testado com artigo, livro e tese; idioma da citação pt-BR (slides 30–31)
- [ ] 5 Aba/menu Zotero visível no editor; Preferências do documento com ABNT (slides 32–33)
- [ ] 6 Estrutura de coleções por etapa e convenção de etiquetas escritas em DECISOES.md (slides 20–21)
- [ ] 7 Pesquisas salvas «sem DOI», «sem PDF», «página da web» criadas (slide 22)
- [ ] 8 Auditoria rodada: scripts/auditar_biblioteca.py sem pendências críticas (slide 49)
- [ ] 9 Convenção de cores das anotações definida; nota extraída com página testada (slides 27–28)
- [ ] 10 Better BibTeX instalado se houver LaTeX/Obsidian; .bib com «Manter atualizado» (slide 38)
- [ ] 11 Backup da pasta de dados feito com o Zotero fechado (scripts/backup_zotero.sh) e rotina agendada (slide 41)
- [ ] 12 Se há coautores: grupo privado criado, permissões e dono definidos (slide 44)
```

## Comandos
| Para | Comando | Evidência |
|---|---|---|
| Auditar | `python3 scripts/auditar_biblioteca.py [--colecao "Nome"] [--csv auditoria.csv]` | saída com «0 com pendências» ou a lista tratada |
| Exportar coleção (BBT) | `bash scripts/exportar_bbt.sh "Nome da coleção" biblatex referencias.bib` | arquivo com N entradas |
| Backup | `bash scripts/backup_zotero.sh [pasta_de_dados] [destino]` (Zotero fechado) | `.tar.gz` datado listado |
| Lista ABNT pela API | `curl "http://127.0.0.1:23119/api/users/0/items/top?format=bib&style=associacao-brasileira-de-normas-tecnicas&locale=pt-BR"` | HTML com `csl-entry` |
| Instalar estilo ABNT sem interface | copiar `modelos/estilos/*.csl` para `<pasta de dados>/styles/` e reiniciar o Zotero | estilo na lista de Configurações → Citação |

## Problema → causa → correção (slide 49)
| Como aparece | Causa | Correção no item |
|---|---|---|
| Título do portal, «Disponível em:», sem periódico | capturado como Página da web | recapturar pelo DOI (varinha) e apagar o item errado |
| Sem DOI na referência | base sem DOI / PDF antigo | buscar na Crossref; preencher só `10.xxxx/…` |
| TÍTULO EM CAIXA ALTA | Scopus/WoS exportam assim | botão direito no título → Caixa de frase |
| «NACIONAL, Agência» | autor institucional em nome/sobrenome | alternar para campo único |
| 2024a/2024b falsos | duplicado | Itens duplicados → Mesclar (nunca excluir) |
| Item some da lista | PDF sem item pai | criar item pai; arrastar o PDF sobre ele |
| Correção some no «Atualizar» | lista editada no Word | corrigir no item; nunca na lista |
| «Erro ao abrir o banco de dados» | pasta de dados em nuvem sincronizada | tirar da pasta; restaurar `zotero.sqlite.bak` |

## Regras
- Nomes de menu em pt-BR como na interface: Editar → Configurações (Geral, Conta, Exportação, Citação, Avançado); Ferramentas → Extensões; botão direito → Encontrar texto completo / Adicionar à Coleção / Adicionar nota a partir de anotações / Criar bibliografia a partir dos itens… / Exportar…
- Sem Java, o suplemento do LibreOffice não instala (log: «unopkg failed»). Instalar um JRE antes.
- Decisões de ferramenta vão para `DECISOES.md` (numeradas e datadas); uso deste agente vai para `USO_DE_IA.csv`.
