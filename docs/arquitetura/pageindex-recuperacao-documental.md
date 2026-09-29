# PageIndex como motor complementar de recuperação documental

**Status:** candidato para avaliação / não adotado como dependência obrigatória  
**Projeto avaliado:** https://github.com/VectifyAI/PageIndex  
**Data da avaliação:** 2026-09-29

## Contexto

O PageIndex é um mecanismo de recuperação documental *vectorless* orientado a raciocínio. Em vez de depender primariamente de chunking + embeddings + busca por similaridade, constrói um índice hierárquico em árvore para o documento e permite que um LLM navegue por essa estrutura para localizar seções relevantes.

A abordagem é especialmente aderente ao ecossistema MirandasTech Pesquisa porque artigos, teses, dissertações, livros e relatórios científicos possuem estrutura explícita: resumo, introdução, revisão, método, resultados, discussão, limitações, apêndices e referências.

## Papel proposto no ecossistema

O PageIndex **não deve substituir toda a camada de busca**. A proposta é usá-lo como motor complementar dentro de uma arquitetura híbrida:

```text
Pergunta de pesquisa
        |
        v
Research Retrieval Router
   |         |          |
   v         v          v
Vector     PageIndex   Busca estruturada
Search     Reasoning   metadados/citações
   |         |          |
   +---------+----------+
             |
             v
     Evidence Composer
             |
             v
  resposta + trechos + fonte
```

### Quando preferir PageIndex

- perguntas sobre **seções específicas** de um trabalho;
- documentos longos ou livros;
- perguntas que exijam distinguir método, resultado, conclusão e limitação;
- extração de evidências em que similaridade semântica isolada possa recuperar trechos parecidos, mas irrelevantes;
- análise de um conjunto previamente selecionado de documentos;
- leitura orientada a contexto, preservando a hierarquia documental.

### Quando preferir busca vetorial ou metadados

- descoberta ampla de papers em grande corpus;
- busca fuzzy por conceitos ou terminologia aproximada;
- recomendação de trabalhos semelhantes;
- filtros bibliográficos (autor, ano, venue, DOI, palavras-chave);
- primeira etapa de triagem antes da leitura profunda.

## Integração com o fluxo científico MirandasTech

Fluxo recomendado:

```text
OpenAlex / Crossref / Scopus / WoS / busca manual
                    |
                    v
              seleção inicial
                    |
        +-----------+-----------+
        |                       |
        v                       v
   Zotero/metadados       PDF/texto completo
        |                       |
        |                       v
        |                   PageIndex
        |                       |
        +-----------+-----------+
                    |
                    v
          Agente Pesquisador
                    |
                    v
      matriz de evidências / notas
                    |
                    v
          Caderno MirandasTech
```

O PageIndex atua na **leitura profunda**, não na descoberta bibliográfica.

## Casos de uso prioritários

1. **Revisão sistemática e mapeamento sistemático**
   - localizar onde cada trabalho descreve método, amostra, métricas e limitações;
   - responder perguntas de extração de dados com rastreabilidade para a seção/página.

2. **Comparação entre artigos**
   - identificar diferenças de metodologia;
   - comparar definições operacionais;
   - levantar evidência favorável e contrária a uma hipótese.

3. **Assistente de leitura científica**
   - perguntas contextuais sobre um artigo;
   - navegação por seção;
   - geração de notas com ligação explícita à evidência.

4. **Produção de síntese**
   - alimentar resumos estruturados;
   - produzir tabelas de evidências;
   - apoiar escrita, sempre mantendo a fonte original como referência primária.

## Arquitetura de avaliação

A avaliação deve comparar pelo menos:

- baseline de busca lexical;
- RAG vetorial atual;
- PageIndex isolado;
- Vector + PageIndex;
- Vector + PageIndex + camada de metadados/citações.

### Métricas

- precisão da recuperação;
- *answer correctness*;
- *citation faithfulness*;
- completude do contexto;
- taxa de alucinação;
- latência;
- tokens e custo por consulta;
- robustez em PDFs longos;
- capacidade de apontar seção/página correta.

## Corpus inicial recomendado

Executar um experimento controlado com 50-100 artigos já utilizados nas linhas de pesquisa MirandasTech, contendo:

- Agentic AI e governança;
- interoperabilidade semântica;
- sistemas multiagentes;
- IA em ITS/portos;
- segurança e auditabilidade.

Criar um conjunto de perguntas com *ground truth* manual e comparar os motores nas mesmas condições.

## Integração técnica

O PageIndex disponibiliza SDK Python e integração com agentes. A integração ideal para o ecossistema MirandasTech é encapsulá-lo atrás de uma interface própria, evitando acoplamento direto da aplicação ao fornecedor/projeto:

```text
DocumentRetrievalProvider
  - index(document)
  - retrieve(query, context)
  - retrieve_sections(query)
  - citations()
```

Implementações possíveis:

- `VectorRetrievalProvider`;
- `PageIndexRetrievalProvider`;
- `HybridRetrievalProvider`.

Isso permite trocar ou combinar mecanismos sem reescrever o Agente Pesquisador.

## Privacidade e implantação

Para documentos científicos públicos, o modo Cloud pode ser avaliado. Para material privado, manuscritos não publicados ou documentos institucionais, priorizar:

1. modo local;
2. controle explícito do provedor de LLM;
3. política de retenção;
4. registro de proveniência;
5. segregação por projeto/usuário.

## Riscos e limitações

- o SDK ainda é classificado pelo próprio projeto como **Alpha**;
- benchmarks publicados pelo fornecedor/projeto devem ser reproduzidos independentemente;
- recuperação baseada em raciocínio pode aumentar latência e custo em certas consultas;
- OCR e documentos intensivos em imagens exigem avaliação específica;
- não elimina a necessidade de gestão bibliográfica, metadados e rastreabilidade acadêmica.

## Decisão arquitetural atual

**Manter PageIndex como tecnologia candidata para PoC e benchmark.**

Não substituir o mecanismo vetorial atual. A direção preferida é uma estratégia **híbrida e roteada por intenção**, em que o sistema escolhe entre busca bibliográfica, busca vetorial e navegação hierárquica por raciocínio.

## Próximos passos

- [ ] selecionar corpus de 50-100 artigos;
- [ ] definir 30-50 perguntas com resposta conhecida;
- [ ] implementar adaptador `PageIndexRetrievalProvider`;
- [ ] registrar latência, custo e acurácia;
- [ ] comparar com baseline vetorial;
- [ ] validar citações e rastreabilidade;
- [ ] decidir adoção no Agente Pesquisador após benchmark.
