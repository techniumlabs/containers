#FROM alpine:3.10.2
FROM alpine@sha256:72c42ed48c3a2db31b7dafe17d275b634664a708d901ec9fd57b1529280f01fb

ARG MAINTAINER
ARG TIMEZONE

LABEL maintainer=${MAINTAINER}

RUN apk --no-cache add tzdata=2019b-r0 && \
  cp "/usr/share/zoneinfo/${TIMEZONE}" /etc/localtime && \
  echo "${TIMEZONE}" > /etc/timezone && apk del tzdata

ENV TERM="xterm" \
  LANG="C.UTF-8" \
  LC_ALL="C.UTF-8"
