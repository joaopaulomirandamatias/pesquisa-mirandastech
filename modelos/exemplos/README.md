# Exemplos preenchidos

Estes arquivos mostram **como fica uma linha preenchida** de cada registro. Não são copiados para o projeto: os modelos que o `iniciar_projeto.py` copia nascem só com o cabeçalho, para que nenhum agente confunda exemplo com dado do seu projeto.

| Arquivo | Uma linha de exemplo de |
|---|---|
| `USO_DE_IA.exemplo.csv` | uso de IA numa triagem assistida (ferramenta, modelo, finalidade, dados enviados, validação, decisão humana, declaração) |
| `registro_exportacoes.exemplo.csv` | uma exportação de base (arquivo, base, conjunto, data, filtros, totais e hash SHA-256) |

Regras que os exemplos ilustram: o hash é calculado com `sha256sum arquivo` depois da exportação; a coluna `declara` vale `declare` ou `nao-declara`; a coluna `quem` recebe as iniciais de quem operou.
