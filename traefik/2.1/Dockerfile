ARG  IMAGE_REGISTRY
ARG  IMAGE_REPOSITORY
FROM ${IMAGE_REGISTRY}/${IMAGE_REPOSITORY}/base:3.10-alpine-r11

ARG TRAEFIK_VERSION="2.1.9"

RUN addgroup -g 1000 traefik && \
  adduser -S -G traefik -u 1000 traefik

RUN set -ex; \
  wget --quiet -O /tmp/traefik.tar.gz "https://github.com/containous/traefik/releases/download/v${TRAEFIK_VERSION}/traefik_v${TRAEFIK_VERSION}_linux_amd64.tar.gz"; \
  tar xzvf /tmp/traefik.tar.gz -C /usr/local/bin traefik; \
  rm -f /tmp/traefik.tar.gz; \
  chmod +x /usr/local/bin/traefik;

USER traefik

EXPOSE 8080
ENTRYPOINT ["traefik"]
