# Manual do plugin — Claude Code, Claude Desktop, Codex e ChatGPT

Manual em slides (40) que ensina a instalar e usar o plugin **Pesquisa MirandasTech** em cada cliente, com capturas reais. Publicado em https://plugin.mirandastech.com.br/ (PDF em /pdf). Hub com todos os manuais: https://www.mirandastech.com.br/pesquisa

- `site/index.html` — o manual pronto (HTML autônomo).
- `fonte/mirandastech_plugin.html` — o fonte do deck (fragmento no motor comum dos manuais MirandasTech); `fonte/gerar_deck.py` gera o HTML autônomo e o PDF (`weasyprint`).
- A Parte 4 (Demonstração) usa quatro animações GIF gravadas numa sessão real no ChatGPT (09/09/2026), em `capturas/demo_0*.gif`, otimizadas para 1200 px com ffmpeg.
- **Capturas, animações e PDF ficam fora do Git**, na release [`manual-assets`](https://github.com/joaopaulomirandamatias/pesquisa-mirandastech/releases/tag/manual-assets) (`manual-assets.zip`, com `capturas/` e `site/manual.pdf`), para não pesar o clone de quem instala o plugin. O `Dockerfile` baixa o zip no build.
- `Dockerfile`, `Caddyfile`, `railway.json` — o serviço estático (pasta raiz do serviço: `manual/`).

Regenerar depois de editar o fonte (na pasta `manual/fonte`):

```bash
python3 gerar_deck.py && cp Manual_Plugin_Pesquisa_Claude_Codex_MirandasTech.html ../site/index.html && cp Manual_Plugin_Pesquisa_Claude_Codex_MirandasTech.pdf ../site/manual.pdf
cd .. && zip -r manual-assets.zip capturas site/manual.pdf && gh release upload manual-assets manual-assets.zip --clobber && rm manual-assets.zip
```
