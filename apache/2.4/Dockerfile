ARG  IMAGE_REGISTRY
ARG  IMAGE_REPOSITORY
FROM ${IMAGE_REGISTRY}/${IMAGE_REPOSITORY}/alpine:3.11-r1

ENV WEB_DOCUMENT_ROOT=/app \
  WEB_DOCUMENT_INDEX=index.php \
  WEB_ALIAS_DOMAIN=*.vm \
  WEB_PHP_TIMEOUT=600 \
  WEB_PHP_SOCKET=""

# hadolint ignore=SC2016
RUN set -eux \
  && addgroup -g 1000 -S apache \
  && adduser -u 1000 -D -S -G apache apache \
  && apk add --no-cache \
  apache2=2.4.43-r0 \
  apache2-ctl=2.4.43-r0 \
  apache2-utils=2.4.43-r0 \
  apache2-proxy=2.4.43-r0 \
  apache2-ssl=2.4.43-r0 \
  && sed -i '2,5{H;d}; ${p;x;s/^\n//}' /etc/apache2/conf.d/proxy.conf \
  && sed -ri ' \
  s!^(\s*CustomLog)\s+\S+!\1 /proc/self/fd/1!g; \
  s!^(\s*ErrorLog)\s+\S+!\1 /proc/self/fd/2!g; \
  ' /etc/apache2/httpd.conf \
  && wget -O "/usr/local/bin/go-replace" "https://github.com/webdevops/goreplace/releases/download/1.1.2/gr-64-linux" \
  && chmod +x "/usr/local/bin/go-replace" \
  && "/usr/local/bin/go-replace" --version

COPY configs /etc/apache2/conf.d/custom
COPY httpd-foreground /usr/local/bin/

# hadolint ignore=SC2016
RUN chmod +x /usr/local/bin/httpd-foreground \
  && go-replace --mode=line --regex --regex-backrefs \
  -s '^[\s#]*(LoadModule mpm_prefork_module.*)' -r '#$1' \
  -s '^[\s#]*(LoadModule mpm_event_module.*)' -r '$1' \
  -s '^[\s#]*(LoadModule deflate_module.*)' -r '$1' \
  -s '^[\s#]*(LoadModule rewrite_module.*)' -r '$1' \
  -s '^[\s#]*(LoadModule logio_module.*)' -r '$1' \
  -s '^[\s#]*(LoadModule slotmem_shm_module.*)' -r '$1' \
  -s '^[\s#]*(LoadModule actions_module.*)' -r '$1' \
  -s '^[\s#]*(LoadModule expires_module.*)' -r '$1' \
  -s '^[\s#]*(LoadModule ssl_module.*)' -r '$1' \
  -s '^[\s#]*(LoadModule socache_shmcb_module.*)' -r '$1' \
  -s '^[\s#]*(LoadModule proxy_ajp_module.*)' -r '#$1' \
  -s '^[\s#]*(LoadModule proxy_connect_module.*)' -r '#$1' \
  -s '^[\s#]*(LoadModule proxy_balancer_module.*)' -r '#$1' \
  -s '^[\s#]*(LoadModule proxy_express_module.*)' -r '#$1' \
  -s '^[\s#]*(LoadModule proxy_fcgi_module.*)' -r '$1' \
  -s '^[\s#]*(LoadModule proxy_fdpass_module.*)' -r '$1' \
  -s '^[\s#]*(LoadModule proxy_ftp_module.*)' -r '$1' \
  -s '^[\s#]*(LoadModule proxy_http_module.*)' -r '$1' \
  -s '^[\s#]*(LoadModule proxy_scgi_module.*)' -r '$1' \
  --  /etc/apache2/httpd.conf \
      /etc/apache2/conf.d/ssl.conf \
  /etc/apache2/conf.d/proxy.conf \
  && sed -i -e '1h;2,$H;$!d;g' -e 's/<VirtualHost.*<\/VirtualHost>/#-> removed vhost/g' /etc/apache2/conf.d/ssl.conf \
  && sed -i 's/Listen 80/Listen 8080/g' /etc/apache2/httpd.conf \
  && sed -i 's/Listen 443/Listen 8443/g' /etc/apache2/conf.d/ssl.conf \
  && find /etc/apache2/conf.d/custom/ssl -type d -exec chmod 750 {} \; \
  && find /etc/apache2/conf.d/custom/ssl -type f -exec chmod 640 {} \; \
  && mv /etc/apache2/conf.d/custom/main.conf /etc/apache2/conf.d/zzz-custom.conf \
  && mkdir -p -- "/var/run/apache2" "/run/apache2" "/env" "/var/www/html" \
  && touch /env/variables \
  && chgrp -R 0 /etc/apache2 /run/apache2 /var/run/apache2 /env /var/www/html \
  && chmod -Rf g=u /etc/apache2 /run/apache2 /var/run/apache2 /env /var/www/html \
  && chown -Rf apache /etc/apache2 /run/apache2 /var/run/apache2 /env /var/www/html \
  && go-replace --regex --regex-backrefs \
  -s '^[\s]*(CustomLog|ErrorLog|TransferLog) ([^\s]+)(.*)' -r '$1 /proc/self/fd/1 $3' \
  -s '^[\s]*(ErrorLog) ([^\s]+)(.*)' -r '$1 /proc/self/fd/2 $3' \
  --path="/etc/apache2" \
  --path-regex='(.*\.conf|default.*|.*log)$'

USER apache
CMD ["httpd-foreground"]

EXPOSE 8080 8443
