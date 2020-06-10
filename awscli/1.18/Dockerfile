ARG  IMAGE_REGISTRY
ARG  IMAGE_REPOSITORY
FROM ${IMAGE_REGISTRY}/${IMAGE_REPOSITORY}/alpine:3.11-r1

RUN apk --no-cache --update add \
  python3=3.8.2-r0 \
  groff=1.22.4-r0 \
  less=551-r0 \
  && pip3 --no-cache-dir install --upgrade awscli==1.18.76 \
  && addgroup -g 1000 awsuser \
  && adduser -u 1000 -G awsuser -s /bin/sh -D awsuser

WORKDIR /project

USER awsuser
