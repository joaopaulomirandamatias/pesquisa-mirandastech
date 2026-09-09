FROM alpine:3.20 AS assets
RUN apk add --no-cache curl unzip
WORKDIR /a
RUN curl -fsSL -o manual-assets.zip https://github.com/joaopaulomirandamatias/pesquisa-mirandastech/releases/download/manual-assets/manual-assets.zip \
 && unzip -q manual-assets.zip

FROM caddy:2-alpine
COPY Caddyfile /etc/caddy/Caddyfile
COPY site/ /srv/
COPY --from=assets /a/capturas/ /srv/capturas/
COPY --from=assets /a/site/manual.pdf /srv/manual.pdf
EXPOSE 8080
ENV PORT=8080
CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
