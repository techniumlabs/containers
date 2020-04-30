ARG  IMAGE_REGISTRY
ARG  IMAGE_REPOSITORY

FROM golang:1.14-alpine AS build

RUN apk add --no-cache git=2.24.3-r0 build-base=0.5-r1
RUN git clone --branch v2.1.3 https://github.com/quay/clair.git
WORKDIR /go/clair/
RUN go build -ldflags "-X github.com/quay/clair/v3/pkg/version.Version=v2.1.3" ./cmd/clair

FROM ${IMAGE_REGISTRY}/${IMAGE_REPOSITORY}/base:3.10-alpine-r17
COPY --from=build /go/clair/clair /clair

RUN mkdir /etc/clair \
  && apk add --no-cache git=2.22.4-r0 rpm=4.13.1-r2 xz=5.2.4-r0

# change ownership of ssl directory to allow custom cert in OpenShift
RUN chgrp -R 0 /etc/ssl/certs /etc/clair && \
chmod -R g=u /etc/ssl/certs /etc/clair

ENTRYPOINT ["cinit", "--", "/clair"]
VOLUME /config
EXPOSE 6060 6061
