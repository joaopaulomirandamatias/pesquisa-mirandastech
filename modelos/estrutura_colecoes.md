# Estrutura de coleções sugerida (slide 20)

```
Projeto 2026/
├── 0 Buscas brutas/            # uma subcoleção por base e data; não mexer depois de importar
│   ├── scopus_2026-09-08
│   └── wos_2026-09-08
├── 1 Triagem/                  # após mesclar duplicados; etiquetas triagem:incluido / triagem:excluido:motivo
├── 2 Incluídos/                # reimportados da triagem; «Encontrar texto completo» aqui
├── 3 Leitura/                  # o que está sendo lido (etiqueta status:lido)
├── 4 Capítulos/                # um por capítulo — o mesmo item pode estar em vários
└── 5 Normas e legislação/
```

Pesquisas salvas de auditoria (slide 22): **sem DOI** (Tipo é Artigo de periódico · DOI não contém «10.»), **sem PDF** (Tipo é Artigo · Anexo não tem arquivo), **página web** (Tipo é Página da web).
