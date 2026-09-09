# Manual do plugin — Claude Code, Claude Desktop, Codex e ChatGPT

Manual em slides (40) que ensina a instalar e usar o plugin **Pesquisa MirandasTech** em cada cliente, com capturas reais de 08/09/2026.

- `site/index.html` — o manual pronto (HTML autônomo); `site/manual.pdf` — a versão em PDF.
- `capturas/` — as capturas de tela usadas nos slides.
- `fonte/mirandastech_plugin.html` — o fonte do deck (fragmento no motor comum dos manuais MirandasTech); `fonte/gerar_deck.py` gera o HTML autônomo e o PDF (`weasyprint`).
- `Dockerfile`, `Caddyfile`, `railway.json` — o serviço estático que publica o manual (pasta raiz do serviço: `manual/`).

Regenerar depois de editar o fonte:

```bash
cd manual/fonte && python3 gerar_deck.py && cp Manual_Plugin_Pesquisa_Claude_Codex_MirandasTech.html ../site/index.html && cp Manual_Plugin_Pesquisa_Claude_Codex_MirandasTech.pdf ../site/manual.pdf
```

Publicado em https://plugin.mirandastech.com.br/ (PDF em /pdf). Hub com todos os manuais: https://www.mirandastech.com.br/pesquisa
