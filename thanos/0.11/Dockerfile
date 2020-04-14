ARG  IMAGE_REGISTRY
ARG  IMAGE_REPOSITORY
FROM ${IMAGE_REGISTRY}/${IMAGE_REPOSITORY}/base:3.10-alpine-r11

ARG THANOS_VERSION="0.11.0"

RUN addgroup -g 1000 thanos && \
  adduser -S -G thanos -u 1000 thanos

RUN set -ex; \
  wget --quiet -O /tmp/thanos.tar.gz "https://github.com/thanos-io/thanos/releases/download/v${THANOS_VERSION}/thanos-${THANOS_VERSION}.linux-amd64.tar.gz"; \
  tar xzvf /tmp/thanos.tar.gz -C /usr/local/bin thanos-${THANOS_VERSION}.linux-amd64/thanos; \
  rm -f /tmp/thanos.tar.gz; \
  chmod +x /usr/local/bin/thanos-${THANOS_VERSION}.linux-amd64/thanos; \
  mv /usr/local/bin/thanos-${THANOS_VERSION}.linux-amd64/thanos /usr/local/bin/thanos; \
  rm -rf /usr/local/bin/thanos-${THANOS_VERSION}.linux-amd64/
USER thanos

EXPOSE 8080
ENTRYPOINT ["thanos"]
