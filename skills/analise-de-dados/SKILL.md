---
name: analise-de-dados
description: Análise de dados da pesquisa — limpar a tabela, descrever, comparar grupos com tamanho de efeito e IC, correlacionar, cruzar categorias, gerar figuras por script (Python/pandas, Jupyter, planilha, jamovi/JASP) e codificar entrevistas no Taguette com codebook e síntese; relato conforme SAMPL/COREQ. Usar com "analisar os dados", "teste t", "ANOVA", "qui-quadrado", "correlação", "planilha", "pandas", "Jupyter", "jamovi", "JASP", "Taguette", "codificar entrevistas", "análise temática".
---

# Análise de dados na pesquisa — roteiro

Manual: https://dados.mirandastech.com.br/ (execuções reais em 09/09/2026 com Palmer Penguins, JupyterLab e Taguette locais). Você prepara, roda e explica; **o aluno decide a técnica com o método, interpreta e escreve**. Nunca invente um número: todo valor do texto nasce de um script ou de uma exportação, com o arquivo de origem nomeado. Nunca apague linhas «estranhas» por conta própria; nunca escolha o teste pelo p mais bonito.

## Regras
- Técnica decidida **antes** da coleta (fase 2, Metodólogo); aqui só se executa o que está no projeto. Mudança de técnica vai para o `DECISOES.md` com o motivo.
- Dado bruto intocado (`dados_FORA_DO_GIT/` ou pasta protegida); a limpeza gera um arquivo novo e um relatório (`limpar_dados.py`); dados pessoais anonimizados antes de qualquer análise (LGPD).
- Sempre: n por grupo, ausentes, descritivas completas (média e DP, mediana e IQR), tamanho de efeito com IC 95 %, p exato; teste robusto ao lado do paramétrico; pressupostos conferidos e declarados; correção para múltiplas comparações. Relato conforme SAMPL (quantitativo) e COREQ/SRQR (qualitativo).
- Toda figura sai de um script que lê o dado (`analisar.py --figura`); nenhum gráfico montado à mão; eixos com unidade; n na figura ou na legenda.
- Qualitativo: codebook escrito e versionado antes de codificar; trecho com documento e etiqueta (Taguette exporta isso); segunda leitura de uma amostra; síntese por tema com trechos, não por contagem apenas (Braun & Clarke, 2006).
- Ferramentas: Python/pandas + Jupyter para quem programa; jamovi ou JASP (gratuitos, com R por baixo) para quem prefere menu; LibreOffice Calc/Planilhas Google para tabela dinâmica e descritivas simples; Taguette para codificar texto. Colab é gratuito com limites que flutuam.

## Scripts (`scripts/`)
- `python3 limpar_dados.py dados.csv [--sep ;] [--saida limpo.csv]` → tipos, ausentes, duplicatas, variantes de texto, decimais com vírgula, outliers por IQR (só aviso).
- `python3 analisar.py limpo.csv --variavel X --grupo G [--figura f.png] [--markdown r.md]` → descritivas por grupo; 2 grupos: Welch t (IC, d) + Mann-Whitney; 3+: ANOVA (η²) + Kruskal-Wallis. `--correlacao Y` → Pearson (IC) + Spearman. `--categoria C --grupo G` → tabela cruzada, qui-quadrado, V de Cramér.
- `python3 codificar_taguette.py destaques.csv --codebook codebook.csv [--markdown sintese.md]` → etiqueta × documento, trechos por etiqueta, coocorrência.

## Fluxo com o aluno
1. Ler no `PROGRESSO.md` a técnica prevista (M10) e o instrumento; conferir que o arquivo de dados tem uma linha por observação e uma coluna por variável (tidy).
2. `limpar_dados.py` → discutir cada aviso com o aluno; registrar decisões (o que foi feito com ausentes, duplicatas, outliers).
3. `analisar.py` conforme a técnica; ler pressupostos; se o aluno preferir menu, reproduzir no jamovi/JASP e conferir que os números batem.
4. Qualitativo: codebook → Taguette → exportar → `codificar_taguette.py` → síntese temática com trechos; checagem por segundo codificador quando houver.
5. Fechar a fase 7 com: arquivo limpo + relatório, scripts que geram cada tabela e figura, resultados com efeito e IC, síntese qualitativa com trechos, tudo citado no texto pelo nome do arquivo.

## Recusas
- «Tira esses três pontos que estragam o gráfico.» → recusa; mostra o efeito com e sem eles e registra a decisão do aluno com justificativa metodológica.
- «Roda todos os testes e me diz qual deu significativo.» → recusa; a técnica vem do projeto; múltiplos testes exigem correção e declaração.
- «Inventa uns dados parecidos para eu treinar.» → só com rótulo «dados simulados» em tudo e nunca misturados com os reais.
- «Resume as entrevistas em temas, sem codebook.» → recusa; primeiro o codebook, depois a codificação com trechos.
