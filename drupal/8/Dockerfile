ARG IMAGE_REGISTRY
ARG IMAGE_REPOSITORY
FROM ${IMAGE_REGISTRY}/${IMAGE_REPOSITORY}/php-fpm:7.2-r3
WORKDIR /data

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

ENV PHPIZE_DEPS \
  autoconf=2.69-r2 \
  dpkg-dev=1.19.7-r1 \
  dpkg=1.19.7-r1 \
  file=5.37-r1 \
  g++=9.2.0-r4 \
  gcc=9.2.0-r4 \
  libc-dev=0.7.2-r0 \
  make=4.2.1-r2 \
  pkgconf=1.6.3-r0 \
  re2c=1.3-r1 \
  libwebp=1.0.3-r0 \
  libwebp-dev=1.0.3-r0 \
  libjpeg=8-r6 \
  libjpeg-turbo-dev=2.0.4-r0 \
  libpng-dev=1.6.37-r1 \
  freetype-dev=2.10.1-r0 \
  libxml2-dev=2.9.10-r3

# hadolint ignore=SC2046,SC2086,DL3003,DL3018
RUN set -eux; \
  apk add --no-cache --virtual .build-deps \
  ${PHPIZE_DEPS} \
  && pecl install apcu \
  && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ \
  --with-jpeg-dir=/usr/include/ --with-png-dir=/usr/include/ --with-webp-dir=/usr/include/ \
  && docker-php-ext-install \
  zip \
  pdo \
  pdo_mysql \
  gd \
  mbstring \
  opcache \
  soap \
  pcntl \
  bcmath \
  && apk del .build-deps \
  && apk add --no-cache \
  libpng=1.6.37-r1 \
  libjpeg=8-r6 \
  libwebp=1.0.3-r0 \
  freetype=2.10.1-r0 \
  make=4.2.1-r2 \
  imagemagick=7.0.9.7-r0

RUN curl -L https://github.com/previousnext/tuner/releases/download/1.0.0/tuner-linux-amd64 -o /usr/local/bin/tuner \
  && chmod +rx /usr/local/bin/tuner

COPY apcu.ini /usr/local/etc/php/conf.d/apcu.ini

COPY php.ini /usr/local/etc/php/php.ini
COPY drushrc.php /etc/drush/drushrc.php

COPY d8.php /var/www/healthz/d8.php

CMD ["octl", "exec", "--","php-fpm"]
