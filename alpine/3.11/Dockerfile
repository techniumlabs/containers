#FROM alpine:3.11.3
FROM alpine@sha256:cb8a924afdf0229ef7515d9e5b3024e23b3eb03ddbba287f4a19c6ac90b8d221

ARG MAINTAINER
ARG TIMEZONE

LABEL maintainer=${MAINTAINER}

RUN apk --no-cache add tzdata=2019c-r0 \
  ca-certificates=20191127-r1 && \
  cp "/usr/share/zoneinfo/${TIMEZONE}" /etc/localtime && \
  echo "${TIMEZONE}" > /etc/timezone && apk del tzdata

ENV TERM="xterm" \
  LANG="C.UTF-8" \
  LC_ALL="C.UTF-8"
