ARG  IMAGE_REGISTRY
ARG  IMAGE_REPOSITORY
FROM ${IMAGE_REGISTRY}/${IMAGE_REPOSITORY}/alpine:v3.10-r1

ARG PROMTAIL_VERSION="1.5.0"

RUN addgroup -g 1000 promtail && \
  adduser -S -G promtail -u 1000 promtail

RUN set -ex; \
  wget --quiet -O /tmp/promtail-linux-amd64.zip "https://github.com/grafana/loki/releases/download/v${PROMTAIL_VERSION}/promtail-linux-amd64.zip" \
  && unzip "/tmp/promtail-linux-amd64.zip" \
  && chmod +x "promtail-linux-amd64" \
  && mv promtail-linux-amd64 /usr/local/bin/promtail \
  && rm /tmp/promtail-linux-amd64.zip \
  && apk add --no-cache libc6-compat=1.1.22-r3

USER promtail
WORKDIR /home/promtail

EXPOSE 8080
ENTRYPOINT ["promtail"]
