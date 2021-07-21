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
       4. [TODO] Azure keyvault
    6. Template Substitution in config file

## Base Images

### Alpine
version 3.10: ![alpine-3.10](https://github.com/techniumlabs/containers/workflows/alpine-3.10/badge.svg)

version 3.11: ![alpine-3.11](https://github.com/techniumlabs/containers/workflows/alpine-3.11/badge.svg)


### Alpine Glibc
version 3.10: ![alpine-glibc-3.10](https://github.com/techniumlabs/containers/workflows/alpine-glibc-3.10/badge.svg)


## PHP

### PHP-FPM
version 7.2: ![php-fpm-7.2](https://github.com/techniumlabs/containers/workflows/php-fpm-7.2/badge.svg)

version 7.3: ![php-fpm-7.3](https://github.com/techniumlabs/containers/workflows/php-fpm-7.3/badge.svg)

version 7.4: ![php-fpm-7.4](https://github.com/techniumlabs/containers/workflows/php-fpm-7.4/badge.svg)


## Reverse Proxies

### Traefik
version 2.0: ![traefik-2.0](https://github.com/techniumlabs/containers/workflows/traefik-2.0/badge.svg)

version 2.1: ![traefik-2.1](https://github.com/techniumlabs/containers/workflows/traefik-2.1/badge.svg)

version 2.2: ![traefik-2.2](https://github.com/techniumlabs/containers/workflows/traefik-2.2/badge.svg)


## Monitoring and Logging
### Thanos
version 0.10: ![thanos-0.10](https://github.com/techniumlabs/containers/workflows/thanos-0.10/badge.svg)

version 0.11: ![thanos-0.11](https://github.com/techniumlabs/containers/workflows/thanos-0.11/badge.svg)

### Loki
version 1.3: ![loki-1.3](https://github.com/techniumlabs/containers/workflows/loki-1.3/badge.svg)

## Security
### Clair
version 2.1: ![clair-2.1](https://github.com/techniumlabs/containers/workflows/clair-2.1/badge.svg)

## Utilties
### Harbor Sync
version 1.3: ![harbor-sync-1.3](https://github.com/techniumlabs/containers/workflows/harbor-sync-1.3/badge.svg)

## Base image validation dependencies 
sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy

## Child image validation and update dependencies
sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy

git config --global user.email "xyz@mail.com"
git config --global user.name "xyz"


git checkout versioning 

pip install --pre azure-containerregistry

pip install --pre azure-identity

pip install gitpython