ARG  IMAGE_REGISTRY
ARG  IMAGE_REPOSITORY
FROM ${IMAGE_REGISTRY}/${IMAGE_REPOSITORY}/base:3.12-alpine-r1

# dependencies required for running "phpize"
# these get automatically installed and removed by "docker-php-ext-*" (unless they're already installed)
ENV PHPIZE_DEPS \
  autoconf=2.69-r2 \
  dpkg-dev=1.19.7-r0 \
  dpkg=1.19.7-r0 \
  file=5.37-r1 \
  g++=8.3.0-r0 \
  gcc=8.3.0-r0 \
  libc-dev=0.7.1-r0 \
  make=4.2.1-r2 \
  pkgconf=1.6.1-r1 \
  re2c=1.1.1-r0

# Apply stack smash protection to functions using local buffers and alloca()
# Make PHP's main executable position-independent (improves ASLR security mechanism, and has no performance impact on x86_64)
# Enable optimization (-O2)
# Enable linker optimization (this sorts the hash buckets to improve cache locality, and is non-default)
# Adds GNU HASH segments to generated executables (this is used if present, and is much faster than sysv hash; in this configuration, sysv hash is also generated)
# https://github.com/docker-library/php/issues/272

ENV PHP_INI_DIR /usr/local/etc/php
ENV PHP_EXTRA_CONFIGURE_ARGS --enable-fpm --with-fpm-user=www-data --with-fpm-group=www-data --disable-cgi
ENV PHP_CFLAGS="-fstack-protector-strong -fpic -fpie -O2"
ENV PHP_CPPFLAGS="$PHP_CFLAGS"
ENV PHP_LDFLAGS="-Wl,-O1 -Wl,--hash-style=both -pie"

ENV GPG_KEYS 5A52880781F755608BF815FC910DEB46F53EA312 42670A7FE4D0441C8E4632349E4FDC074A4EF02D

ENV PHP_VERSION 7.4.5
ENV PHP_URL="https://github.com/techniumlabs/php-releases/releases/download/7.4.5/php-7.4.5.tar.xz" PHP_ASC_URL="https://github.com/techniumlabs/php-releases/releases/download/7.4.5/php-7.4.5.tar.xz.asc"
ENV PHP_SHA256="d059fd7f55bdc4d2eada15a00a2976697010d3631ef6f83149cc5289e1f23c2c" PHP_MD5=""

COPY docker-php-* /usr/local/bin/

# persistent / runtime deps
RUN apk add --no-cache \
  curl \
  tar\
  xz

# ensure www-data user exists
RUN set -eux; \
  addgroup -g 82 -S www-data; \
  adduser -u 82 -D -S -G www-data www-data; \
  mkdir -p "$PHP_INI_DIR/conf.d"; \
  mkdir -p /var/www/html; \
  chown www-data:www-data /var/www/html; \
  chmod 777 /var/www/html; \
  mkdir -p /env; \
  chgrp -R 0 /env; \
  chmod -Rf u=g /env

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]
# hadolint ignore=DL3003
RUN set -eux; \
  apk add --no-cache --virtual .fetch-deps gnupg=2.2.19-r0; \
  \
  mkdir -p /usr/src; \
  cd /usr/src; \
  \
  curl -fSL --retry 5 -o php.tar.xz "$PHP_URL"; \
#   \
#   if [ -n "$PHP_SHA256" ]; then \
#     echo "$PHP_SHA256 *php.tar.xz" | sha256sum -c -; \
#   fi; \
#   if [ -n "$PHP_MD5" ]; then \
#     echo "$PHP_MD5 *php.tar.xz" | md5sum -c -; \
#   fi; \
#   \
#   if [ -n "$PHP_ASC_URL" ]; then \
#     curl -fSL --retry 5 -o php.tar.xz.asc "$PHP_ASC_URL"; \
#     GNUPGHOME="$(mktemp -d)"; \
#     export GNUPGHOME; \
#     for key in $GPG_KEYS; do \
#        gpg --batch --keyserver ha.pool.sks-keyservers.net --recv-keys "$key"; \
#     done; \
#     gpg --batch --verify php.tar.xz.asc php.tar.xz; \
#     gpgconf --kill all; \
#     rm -rf "$GNUPGHOME"; \
#   fi; \
#   \
  apk del --no-network .fetch-deps


# hadolint ignore=SC2046,SC2086,DL3003,DL3018
RUN set -eux; \
  apk add --no-cache --virtual .build-deps \
  ${PHPIZE_DEPS} \
  argon2-dev \
  coreutils \
  curl-dev \
  libedit-dev \
  libsodium-dev \
  libxml2-dev \
  linux-headers \
  oniguruma-dev \
  sqlite-dev \
  ; \
  \
  export CFLAGS="$PHP_CFLAGS" \
    CPPFLAGS="$PHP_CPPFLAGS" \
    LDFLAGS="$PHP_LDFLAGS" \
  ; \
  docker-php-source extract; \
  cd /usr/src/php; \
  gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)"; \
  ./configure \
    --build="$gnuArch" \
    --with-config-file-path="$PHP_INI_DIR" \
    --with-config-file-scan-dir="$PHP_INI_DIR/conf.d" \
    \
# make sure invalid --configure-flags are fatal errors intead of just warnings
    --enable-option-checking=fatal \
    \
# https://github.com/docker-library/php/issues/439
    --with-mhash \
    \
# --enable-ftp is included here because ftp_ssl_connect() needs ftp to be compiled statically (see https://github.com/docker-library/php/issues/236)
    --enable-ftp \
# --enable-mbstring is included here because otherwise there's no way to get pecl to use it properly (see https://github.com/docker-library/php/issues/195)
    --enable-mbstring \
# --enable-mysqlnd is included here because it's harder to compile after the fact than extensions are (since it's a plugin for several extensions, not an extension in itself)
    --enable-mysqlnd \
# https://wiki.php.net/rfc/argon2_password_hash (7.2+)
    --with-password-argon2 \
# https://wiki.php.net/rfc/libsodium
    --with-sodium=shared \
    \
    --with-curl \
    --with-libedit \
    --with-openssl \
    --with-zlib \
    --with-pear \
    \
# bundled pcre does not support JIT on s390x
# https://manpages.debian.org/stretch/libpcre3-dev/pcrejit.3.en.html#AVAILABILITY_OF_JIT_SUPPORT
    $(test "$gnuArch" = 's390x-linux-musl' && echo '--without-pcre-jit') \
    \
    ${PHP_EXTRA_CONFIGURE_ARGS:-} \
  ; \
  make -j "$(nproc)"; \
  find . -type f -name '*.a' -delete; \
  make install; \
  find /usr/local/bin /usr/local/sbin -type f -perm +0111 -exec strip --strip-all '{}' + || true; \
  make clean; \
  \
# https://github.com/docker-library/php/issues/692 (copy default example "php.ini" files somewhere easily discoverable)
  cp -v php.ini-* "$PHP_INI_DIR/"; \
  \
  cd /; \
  docker-php-source delete; \
  \
  runDeps="$( \
    scanelf --needed --nobanner --format '%n#p' --recursive /usr/local \
      | tr ',' '\n' \
      | sort -u \
      | awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 { next } { print "so:" $1 }' \
  )"; \
  apk add --no-cache $runDeps; \
  \
  apk del --no-network .build-deps; \
  \
# update pecl channel definitions https://github.com/docker-library/php/issues/443
  pecl update-channels; \
  rm -rf /tmp/pear ~/.pearrc; \
# smoke test
  php --version

WORKDIR /var/www/html

# hadolint ignore=DL3003
RUN set -eux; \
  docker-php-ext-enable sodium; \
  cd /usr/local/etc; \
  if [ -d php-fpm.d ]; then \
    # for some reason, upstream's php-fpm.conf.default has "include=NONE/etc/php-fpm.d/*.conf"
    sed 's!=NONE/!=!g' php-fpm.conf.default | tee php-fpm.conf > /dev/null; \
    cp php-fpm.d/www.conf.default php-fpm.d/www.conf; \
  else \
    # PHP 5.x doesn't use "include=" by default, so we'll create our own simple config that mimics PHP 7+ for consistency
    mkdir php-fpm.d; \
    cp php-fpm.conf.default php-fpm.d/www.conf; \
    { \
      echo '[global]'; \
      echo 'include=etc/php-fpm.d/*.conf'; \
    } | tee php-fpm.conf; \
  fi; \
  { \
    echo '[global]'; \
    echo 'error_log = /proc/self/fd/2'; \
    echo; \
    echo '[www]'; \
    echo '; if we send this to /proc/self/fd/1, it never appears'; \
    echo 'access.log = /proc/self/fd/2'; \
    echo; \
    echo 'clear_env = no'; \
    echo; \
    echo '; Ensure worker stdout and stderr are sent to the main error log.'; \
    echo 'catch_workers_output = yes'; \
  } | tee php-fpm.d/docker.conf; \
  { \
    echo '[global]'; \
    echo 'daemonize = no'; \
    echo; \
    echo '[www]'; \
    echo 'listen = 9000'; \
    echo 'pm.start_servers = 5'; \
    echo 'pm.min_spare_servers = 3'; \
    echo 'pm.max_spare_servers = 6'; \
    echo 'pm.max_children = 25'; \
  } | tee php-fpm.d/zz-docker.conf

# Override stop signal to stop process gracefully
# https://github.com/php/php-src/blob/17baa87faddc2550def3ae7314236826bc1b1398/sapi/fpm/php-fpm.8.in#L163
STOPSIGNAL SIGQUIT

ONBUILD USER root

ENTRYPOINT ["docker-php-entrypoint"]
EXPOSE 9000

USER www-data

CMD ["/bin/sh", "-c", "source /env/variables; php-fpm"]
# last_updated_date=2021-06-29 02:21:05.502225