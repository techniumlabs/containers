ARG  IMAGE_REGISTRY
ARG  IMAGE_REPOSITORY
FROM ${IMAGE_REGISTRY}/${IMAGE_REPOSITORY}/alpine:3.11-r1

ARG MAINTAINER
LABEL maintainer=${MAINTAINER}

RUN  apk add --no-cache redis=5.0.7-r0 \
    &&  mkdir /data && chown redis:redis /data
VOLUME /data
WORKDIR /data

COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 6379
CMD ["redis-server"]
