#FROM alpine:3.10.4
FROM alpine@sha256:de78803598bc4c940fc4591d412bffe488205d5d953f94751c6308deeaaa7eb8

ARG MAINTAINER
ARG TIMEZONE

LABEL maintainer=${MAINTAINER}

RUN apk --no-cache add tzdata=2019c-r0 \
  ca-certificates=20191127-r0 \
  && cp "/usr/share/zoneinfo/${TIMEZONE}" /etc/localtime \
  && echo "${TIMEZONE}" > /etc/timezone \
  && apk del tzdata \
  && wget -O /tmp/cinit.tar.gz https://github.com/techniumlabs/cinit/releases/download/v0.0.1/cinit_0.0.1_linux_x86_64.tar.gz \
  && tar -xzvf /tmp/cinit.tar.gz -C /tmp \
  && mv /tmp/cinit /usr/local/bin/cinit \
  && chmod +x /usr/local/bin/cinit

ENV TERM="xterm" \
  LANG="C.UTF-8" \
  LC_ALL="C.UTF-8"
