ARG  IMAGE_REGISTRY
ARG  IMAGE_REPOSITORY
FROM ${IMAGE_REGISTRY}/${IMAGE_REPOSITORY}/base:alpine-3.10.2-r0

WORKDIR /usr/src

RUN apk add --no-cache \
  curl=7.66.0-r0 \
  jq=1.6-r0

RUN mkdir /env

RUN addgroup vault && \
  adduser -S -G vault vault

COPY vault-get-secrets.sh /usr/src/
RUN chmod u+x /usr/src/vault-get-secrets.sh && \
  chgrp -R 0 /usr/src

USER vault
CMD [ "/usr/src/vault-get-secrets.sh" ]
