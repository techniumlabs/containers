#FROM alpine:3.12
FROM alpine@sha256:a15790640a6690aa1730c38cf0a440e2aa44aaca9b0e8931a9f2b0d7cc90fd65

ARG MAINTAINER
ARG TIMEZONE

LABEL maintainer=${MAINTAINER}

RUN apk --no-cache add tzdata=2020a-r0 \
  openssl=1.1.1g-r0 \
  openssl-dev=1.1.1g-r0 \
  ca-certificates=20191127-r4 \
  && cp "/usr/share/zoneinfo/${TIMEZONE}" /etc/localtime \
  && echo "${TIMEZONE}" > /etc/timezone \
  && apk del tzdata \
  && wget -O /tmp/cinit.tar.gz https://github.com/techniumlabs/cinit/releases/download/v0.0.1/cinit_0.0.1_linux_x86_64.tar.gz \
  && tar -xzvf /tmp/cinit.tar.gz -C /tmp \
  && mv /tmp/cinit /usr/local/bin/cinit \
  && chmod +x /usr/local/bin/cinit \
  && rm -Rf /tmp/*

ENV TERM="xterm" \
LANG="C.UTF-8" \
LC_ALL="C.UTF-8"

COPY bin/octl-linux-amd64 /usr/bin/octl
RUN chmod +x /usr/bin/octl
