# Containers
    This repository contains dockerfiles for docker containers that is widely used.

## Why ?
    The images built are with the following in mind.

    1. Deterministic builds
    2. Tested Builds
    3. Continuous Patching
    4. Linted
    5. Support for injecting secrets via secret manager
       1. Vault
       2. AWS Secret Manager
       3. AWS Parameter Store
    6. Template Substitution in config file

## Base Images

### Alpine
version 3.10: ![Alpine 3.10 Image](https://github.com/techniumlabs/containers/workflows/Alpine%203.10%20Image/badge.svg)

version 3.11: ![Alpine 3.11 Image](https://github.com/techniumlabs/containers/workflows/Alpine%203.11%20Image/badge.svg)


### Alpine Glibc
version 3.10: ![Alpine glibc 3.10 Image](https://github.com/techniumlabs/containers/workflows/Alpine%20glibc%203.10%20Image/badge.svg)


## PHP

### PHP-FPM
version 7.2: ![PHP FPM 7.2 Image](https://github.com/techniumlabs/containers/workflows/PHP%20FPM%207.2%20Image/badge.svg)

version 7.3: ![PHP FPM 7.3 Image](https://github.com/techniumlabs/containers/workflows/PHP%20FPM%207.3%20Image/badge.svg)

version 7.4: ![PHP FPM 7.4 Image](https://github.com/techniumlabs/containers/workflows/PHP%20FPM%207.4%20Image/badge.svg)


## Reverse Proxies

### Traefik
version 2.0: ![Traefik 2.0 Image](https://github.com/techniumlabs/containers/workflows/Traefik%202.0%20Image/badge.svg)

version 2.1: ![Traefik 2.1 Image](https://github.com/techniumlabs/containers/workflows/Traefik%202.1%20Image/badge.svg)

version 2.2: ![Traefik 2.2 Image](https://github.com/techniumlabs/containers/workflows/Traefik%202.2%20Image/badge.svg)


## Monitoring and Logging
### Thanos
version 0.11: ![Thanos 0.11.1Image](https://github.com/techniumlabs/containers/workflows/Thanos%200.11.1Image/badge.svg)

version 0.10: ![Thanos 0.10.1Image](https://github.com/techniumlabs/containers/workflows/Thanos%200.10.1Image/badge.svg)

### Loki
version 1.3: ![Loki 1.3 Image](https://github.com/techniumlabs/containers/workflows/Loki%201.3%20Image/badge.svg)

## Security
### Clair
version 2.1: ![clair 2.1 Image](https://github.com/techniumlabs/containers/workflows/clair%202.1%20Image/badge.svg)
