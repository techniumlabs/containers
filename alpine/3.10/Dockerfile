#FROM alpine:3.10.4
FROM alpine@sha256:de78803598bc4c940fc4591d412bffe488205d5d953f94751c6308deeaaa7eb8

ARG MAINTAINER
ARG TIMEZONE

LABEL maintainer=${MAINTAINER}

RUN apk --no-cache add tzdata=2019c-r0 \
  ca-certificates=20190108-r0 && \
  cp "/usr/share/zoneinfo/${TIMEZONE}" /etc/localtime && \
  echo "${TIMEZONE}" > /etc/timezone && apk del tzdata

ENV TERM="xterm" \
  LANG="C.UTF-8" \
  LC_ALL="C.UTF-8"
