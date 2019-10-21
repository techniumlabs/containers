ARG IMAGE_REGISTRY
ARG IMAGE_REPOSITORY
FROM ${IMAGE_REGISTRY}/${IMAGE_REPOSITORY}/base:ubuntu-bionic-r0

ARG AGENT_VERSION=2.158.0

# To make it easier for build and release pipelines to run apt-get,
# configure apt to not require confirmation (assume the -y argument by default)
ENV DEBIAN_FRONTEND=noninteractive
RUN echo "APT::Get::Assume-Yes \"true\";" > /etc/apt/apt.conf.d/90assumeyes

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  ca-certificates=20180409 \
  curl=7.58.0-2ubuntu3.8 \
  jq=1.5+dfsg-2 \
  git=1:2.17.1-1ubuntu0.4 \
  iputils-ping=3:20161105-1ubuntu3 \
  libicu60=60.2-3ubuntu3 \
  libunwind8=1.2.1-8 \
  netcat=1.10-41.1 \
  openssl1.0=1.0.2n-1ubuntu5.3 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /azp
COPY ./start.sh .
RUN curl -O "https://vstsagentpackage.azureedge.net/agent/${AGENT_VERSION}/vsts-agent-linux-x64-${AGENT_VERSION}.tar.gz" \
  && tar zxvf "vsts-agent-linux-x64-${AGENT_VERSION}.tar.gz" \
  && chmod +x start.sh \
  && useradd azure \
  && mkdir /env \
  && chown -Rf azure:azure /azp \
  && chgrp -R 0 /azp /env \
  && chmod -Rf g=u /azp /env

USER azure

CMD ["./start.sh"]
