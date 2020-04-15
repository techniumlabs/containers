ARG  IMAGE_REGISTRY
ARG  IMAGE_REPOSITORY
FROM ${IMAGE_REGISTRY}/${IMAGE_REPOSITORY}/base:3.10-alpine-r10

ARG HARBORSYNC_VERSION="1.3.2"

RUN addgroup -g 1000 harborsync && \
  adduser -S -G harborsync -u 1000 harborsync

RUN set -ex; \
  wget --quiet -O /tmp/harborsync.tar.gz "https://github.com/moolen/harbor-sync/releases/download/v1.3.2/harbor-sync-controller.tar.gz"; \
  tar xzvf /tmp/harborsync.tar.gz -C /usr/local bin/harbor-sync-controller; \
  rm -f /tmp/harborsync.tar.gz; \
  chmod +x /usr/local/bin/harbor-sync-controller;

USER harborsync

EXPOSE 8080
ENTRYPOINT ["harborsync"]