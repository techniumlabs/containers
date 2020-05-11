import yaml

with open('apps.yaml', 'r') as fp:
    appconfig = yaml.load(fp)

for app in appconfig['apps']:
    for version in app['versions']:
        workflow = f'''
name: {app['name']}-{version['name']}
on:
  push:
    branches:
      - master
    tags:
      - '{app["name"]}/{version["name"]}/*'
    paths:
      - '{app["name"]}/{version["name"]}/**'
      - '.github/workflows/{app["name"]}-{version["name"]}.yml'

env:
  IMAGE_DIR: {app['name']}/{version['name']}
  IMAGE_NAME: {app['name']}
  IMAGE_VERSION: {version['name']}-r${{{{github.run_number}}}}
  IMAGE_REGISTRY: docker.pkg.github.com/techniumlabs
  IMAGE_REPOSITORY: containers
  MAINTAINER: devops@techniumlabs.com
  TIMEZONE: Australia/Sydney

jobs:
  release:
    runs-on: ubuntu-latest
    if: github.event_name == 'push'

    steps:
      - uses: actions/checkout@v2

      - name: Log into registry
        run: echo "${{{{ secrets.GITHUB_TOKEN }}}}" | docker login docker.pkg.github.com -u ${{{{ github.actor }}}} --password-stdin

      - name: Lint Dockerfile
        run: docker run --rm -i hadolint/hadolint < ${{IMAGE_DIR}}/Dockerfile

      - name: Build image
        run: docker build --file ${{IMAGE_DIR}}/Dockerfile
              --label "org.opencontainers.image.source=https://github.com/techniumlabs/containers/${{IMAGE_DIR}}"
              --label "org.opencontainers.image.revision=${{{{ github.sha }}}}"
              --label "org.opencontainers.image.vendor=techniumlabs"
              --build-arg IMAGE_REGISTRY=${{IMAGE_REGISTRY}}
              --build-arg IMAGE_REPOSITORY=${{IMAGE_REPOSITORY}}
              --build-arg MAINTAINER=${{MAINTAINER}}
              --build-arg TIMEZONE=${{TIMEZONE}}
              --tag image ${{IMAGE_DIR}}

      - name: Install trivy
        run: |
          export VERSION=$(curl --silent "https://api.github.com/repos/aquasecurity/trivy/releases/latest" | grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\\1/')
          wget https://github.com/aquasecurity/trivy/releases/download/v${{VERSION}}/trivy_${{VERSION}}_Linux-64bit.tar.gz
          tar zxvf trivy_${{VERSION}}_Linux-64bit.tar.gz

      - name: Scan Container
        run: |
          ./trivy --exit-code 0 --severity UNKNOWN,LOW,MEDIUM --no-progress image
          ./trivy --exit-code 1 --severity HIGH,CRITICAL --no-progress image

      - name: Push image
        run: |
          IMAGE_ID=docker.pkg.github.com/${{{{ github.repository }}}}/$IMAGE_NAME

          echo IMAGE_ID=$IMAGE_ID
          echo IMAGE_VERSION=$IMAGE_VERSION

          docker tag image $IMAGE_ID:$IMAGE_VERSION
          docker push $IMAGE_ID:$IMAGE_VERSION

      - name: Login to docker hub
        run: echo "${{{{ secrets.DOCKER_PASSWORD }}}}" | docker login --username ${{{{ secrets.DOCKER_USERNAME }}}} --password-stdin

      - name: Push image to docker hub
        run: |
          IMAGE_ID=techniumlabs/$IMAGE_NAME
          echo IMAGE_ID=$IMAGE_ID
          echo IMAGE_VERSION=$IMAGE_VERSION
          docker tag image $IMAGE_ID:$IMAGE_VERSION
          docker push $IMAGE_ID:$IMAGE_VERSION

        '''
        with open(f'.github/workflows/{app["name"]}-{version["name"]}.yml', 'w') as fp:
            fp.write(workflow)