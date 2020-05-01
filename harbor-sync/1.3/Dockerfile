ARG  IMAGE_REGISTRY
ARG  IMAGE_REPOSITORY

# Golang build container
FROM golang:1.14-alpine as gobuilder

RUN apk add --no-cache gcc=9.2.0-r4 g++=9.2.0-r4 git=2.24.3-r0

WORKDIR $GOPATH/src/github.com/moolen
RUN git clone --branch v1.3.2 https://github.com/moolen/harbor-sync.git

WORKDIR $GOPATH/src/github.com/moolen/harbor-sync
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 GO111MODULE=on go build -a -o harbor-sync-controller main.go \
  && cp harbor-sync-controller /usr/local/bin/harbor-sync-controller

FROM ${IMAGE_REGISTRY}/${IMAGE_REPOSITORY}/base:3.10-alpine-r17
ARG HARBORSYNC_VERSION="1.3.2"

RUN addgroup -g 1000 harborsync && \
  adduser -S -G harborsync -u 1000 harborsync

COPY --from=gobuilder /usr/local/bin/harbor-sync-controller /usr/local/bin/harbor-sync-controller
RUN chmod +x /usr/local/bin/harbor-sync-controller

# RUN set -ex; \
#   wget --quiet -O /tmp/harborsync.tar.gz "https://github.com/moolen/harbor-sync/releases/download/v1.3.2/harbor-sync-controller.tar.gz"; \
#   tar xzvf /tmp/harborsync.tar.gz -C /usr/local bin/harbor-sync-controller; \
#   rm -f /tmp/harborsync.tar.gz; \
#   chmod +x /usr/local/bin/harbor-sync-controller;

USER harborsync
WORKDIR /home/harborsync
COPY cinit.yaml /home/harborsync/.cinit.yaml

ENTRYPOINT ["cinit", "--", "harbor-sync-controller"]
