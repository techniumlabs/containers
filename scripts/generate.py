import yaml

with open('apps.yaml', 'r') as fp:
    appconfig = yaml.load(fp)

for app in appconfig['apps']:
    for version in app['versions']:
        workflow = f'''name: {app['name']}-{version['name']}
on:
  create:
  push:
    branches:
      - master
    paths:
      - '{app["name"]}/{version["name"]}/**'
      - '.github/workflows/{app["name"]}-{version["name"]}.yml'

env:
  IMAGE_VERSION: {version['name']}-r${{{{github.run_number}}}}
  IMAGE_REGISTRY: registry.hub.docker.com
  IMAGE_REPOSITORY: techniumlabs
  MAINTAINER: devops@techniumlabs.com
  TIMEZONE: Australia/Sydney

jobs:
  ci-build:
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    steps:
      - uses: actions/checkout@v2
      - name: Publish to registry
        uses: ./action
        with:
          name: {app["name"]}
          registry: docker.pkg.github.com/techniumlabs/containers
          username: ${{{{ github.actor }}}}
          password: ${{{{ secrets.GITHUB_TOKEN }}}}
          workdir: {app["name"]}/{version["name"]}
          buildargs: IMAGE_REGISTRY,IMAGE_REPOSITORY,MAINTAINER,TIMEZONE
          tags: {version["name"]}-ci-build-r${{{{ github.sha }}}}
  release-build:
    runs-on: ubuntu-latest
    if: github.event_name == 'create' && startswith(github.ref, 'refs/tags/{app["name"]}/{version["name"]}/')
    steps:
      - uses: actions/checkout@v2
      - name: Publish to docker registry
        uses: ./action
        with:
          name: techniumlabs/{app["name"]}
          version: '{version["name"]}'
          username: ${{{{ secrets.DOCKER_USERNAME }}}}
          password: ${{{{ secrets.DOCKER_PASSWORD }}}}
          workdir: {app["name"]}/{version["name"]}
          buildargs: IMAGE_REGISTRY,IMAGE_REPOSITORY,MAINTAINER,TIMEZONE
          tag_names: true'''
        with open(f'.github/workflows/{app["name"]}-{version["name"]}.yml', 'w') as fp:
            fp.write(workflow)
