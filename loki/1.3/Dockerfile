ARG  IMAGE_REGISTRY
ARG  IMAGE_REPOSITORY
FROM ${IMAGE_REGISTRY}/${IMAGE_REPOSITORY}/base:3.10-alpine-r11

ARG LOKI_VERSION="1.3.0"

RUN addgroup -g 1000 loki && \
  adduser -S -G loki -u 1000 loki

RUN set -ex; \
  wget --quiet -O /tmp/loki-linux-amd64.zip "https://github.com/grafana/loki/releases/download/v${LOKI_VERSION}/loki-linux-amd64.zip"; \
  unzip "/tmp/loki-linux-amd64.zip";\
  chmod +x "loki-linux-amd64";\
  mv loki-linux-amd64 /usr/local/bin/loki;

USER loki

EXPOSE 8080
ENTRYPOINT ["loki"]
