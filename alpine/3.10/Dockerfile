#FROM alpine:3.10.4
FROM alpine:3.10.4

ARG MAINTAINER
ARG TIMEZONE=us

LABEL maintainer=${MAINTAINER}

RUN echo "${TIMEZONE}"

RUN apk --no-cache add tzdata=2020a-r0 \
  openssl \
  openssl-dev \
  ca-certificates \
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
