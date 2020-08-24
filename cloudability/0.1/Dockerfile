ARG  IMAGE_REGISTRY
ARG  IMAGE_REPOSITORY

FROM golang:1.14-alpine as build-env

RUN apk add --no-cache git=2.26.2-r0

WORKDIR $GOPATH/src/github.com/cloudability
RUN git clone --branch master https://github.com/cloudability/metrics-agent.git

WORKDIR $GOPATH/src/github.com/cloudability/metrics-agent

# Build source code
RUN CGO_ENABLED=0 GOOS=linux go build

FROM ${IMAGE_REGISTRY}/${IMAGE_REPOSITORY}/alpine:3.11-r1

RUN addgroup -g 1000 agent && \
    adduser agent -S -u 1000 -s /bin/nologin -g metrics-agent -H -G agent 

WORKDIR /

COPY --from=build-env /go/src/github.com/cloudability/metrics-agent/metrics-agent /metrics-agent

USER agent

ENTRYPOINT ["/metrics-agent"]