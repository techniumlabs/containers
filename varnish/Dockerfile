ARG  IMAGE_REGISTRY
ARG  IMAGE_REPOSITORY
FROM ${IMAGE_REGISTRY}/${IMAGE_REPOSITORY}/base:alpine-3.10.2-r9

RUN set -x \
  && apk add --no-cache \
  varnish=6.2.1-r0

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh \
  && mkdir -p /var/lib/varnish /var/log/varnish \
  && chgrp -R 0 /var/lib/varnish /var/log/varnish \
  && chmod -Rf g=u /var/lib/varnish /var/log/varnish

ENTRYPOINT ["docker-entrypoint.sh"]

USER varnish

cmd ["varnishd", "-a", "localhost:6081", "-f", "/etc/varnish/default.vcl"]
