# Prompts e modelos do manual «Gemini Notebook para pesquisa científica»

Copie na caixa «Faça uma pergunta ou crie algo» e adapte os colchetes. Todo prompt pede escopo (fontes selecionadas), formato e o que fazer na falta («não informado»).

## prompt — inventário das fontes (teste de ingestão)

```text
Para cada fonte deste notebook, liste em uma tabela:
nome da fonte · tipo de documento (artigo, capítulo, norma, site…) ·
autores e ano, se constarem · objetivo declarado em uma frase ·
número aproximado de páginas ou seções que você consegue ver.
Se alguma fonte estiver vazia, ilegível ou contiver só um resumo,
diga isso explicitamente na linha dela.
```

## estilo «Personalizado» — instrução sugerida para pesquisa

```text
Você responde apenas com base nas fontes selecionadas deste notebook.
Responda em português do Brasil. Quando a informação não estiver nas
fontes, escreva «não informado nas fontes» em vez de completar.
Sempre cite o trecho. Prefira tabelas quando eu pedir comparação.
Não use adjetivos avaliativos («excelente», «robusto») que as fontes não usem.
```

## prompt — tabela de triagem (Conversa ou Tabela de dados)

```text
Monte uma tabela com uma linha por fonte e estas colunas:
fonte · ano · país ou contexto · o que o estudo mede (variável ou
fenômeno principal) · desenho do estudo · população ou amostra (n) ·
instrumento ou fonte de dados · resultado principal em uma frase ·
limitação declarada pelos autores.
Use «não informado» quando a fonte não trouxer o dado.
Não classifique a relevância; não omita nenhuma fonte.
```

## prompt — fichamento guiado do artigo selecionado

```text
Considere apenas a fonte selecionada. Responda em tópicos, um por
seção (Introdução, Métodos, Resultados, Discussão), sempre com a
citação do trecho. Em «Resultados», traga os números e a tabela ou
figura de origem. Em «Discussão», separe: (a) o que os autores
afirmam ter demonstrado; (b) limitações que eles declaram;
(c) sugestões para estudos futuros. Não avalie o artigo.
```

## prompt — matriz de síntese (colunas do protocolo)

```text
Preencha uma tabela com uma linha por fonte selecionada e as colunas:
[pergunta 1 da revisão] · [pergunta 2] · [pergunta 3] ·
contexto do estudo · método · amostra · resultado principal ·
limitação declarada.
Uma frase por célula, com a citação. Escreva «não informado»
quando a fonte não responder à pergunta. Não resuma entre fontes;
não acrescente fontes que não estejam selecionadas.
```

## prompt — roteiro de aula em três blocos

```text
A partir das fontes selecionadas, proponha um roteiro de aula de
[50] minutos em três blocos (conceito, método, aplicação). Para cada
bloco: objetivo de aprendizagem em uma frase, os dois ou três pontos
essenciais com a citação da fonte, um exemplo que as fontes tragam
e uma pergunta para discussão. Não invente exemplos fora das fontes.
```

## prompt — perguntas prováveis da banca

```text
Leia a fonte selecionada como um examinador. Liste 20 perguntas que
uma banca faria, agrupadas em: objetivo e problema; método e
amostra; resultados e sua interpretação; limitações; contribuição
e trabalhos futuros. Para cada pergunta, cite o trecho da tese que a
motivou e diga se o texto já responde a ela (sim, parcialmente, não).
```

## declaração — modelo mínimo (adapte ao programa)

```text
Na etapa de leitura e síntese da literatura, utilizou-se o Gemini
Notebook (Google) para localizar trechos e organizar uma matriz de
extração a partir dos [n] estudos incluídos. Todas as informações
extraídas foram conferidas nos textos originais pelo(a) autor(a).
A ferramenta não foi usada para buscar literatura, decidir critérios
de inclusão nem redigir o texto.
```
