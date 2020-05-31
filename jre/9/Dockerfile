ARG IMAGE_REGISTRY
ARG IMAGE_REPOSITORY
FROM ${IMAGE_REGISTRY}/${IMAGE_REPOSITORY}/alpine-glibc:3.11-r1

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

ARG JRE_DOWNLOAD_URL="https://github.com/AdoptOpenJDK/openjdk9-binaries/releases/download/jdk-9+181/OpenJDK9U-jre_x64_linux_hotspot_9_181.tar.gz"
ARG JRE_SHA256=b6a14f8dda60528bbb890877b62b7cf6e81bbbe19256bfd38a3ba4390c4eca5e

ENV JAVA_HOME /opt/java/jdk9-jre
ENV PATH $JAVA_HOME/bin:$PATH

# hadolint ignore=DL3003
RUN set -eux \
  && addgroup -g 1000 javauser \
  && adduser -u 1000 -G javauser -s /bin/sh -D javauser \
  && apk add --no-cache --virtual .fetch-deps curl=7.67.0-r0 \
  && curl -LfsSo /tmp/openjdk.tar.gz "${JRE_DOWNLOAD_URL}" \
  && echo "${JRE_SHA256} */tmp/openjdk.tar.gz" | sha256sum -c -

# hadolint ignore=DL3003
RUN mkdir -p /opt/java \
  && cd /opt/java \
  && tar -xzvf /tmp/openjdk.tar.gz \
  && mv jdk-9+181-jre jdk9-jre \
  && chown -R javauser:0 /opt/java \
  && apk add --no-cache java-cacerts=1.0-r0 \
  && ln -sf /etc/ssl/certs/java/cacerts "${JAVA_HOME}/lib/security/cacerts" \
  && apk del --purge .fetch-deps \
  && rm -rf /var/cache/apk/* \
  && rm -rf /tmp/openjdk.tar.gz

USER javauser
