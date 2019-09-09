SHELL					:= /bin/bash
WORKING_DIR   := $(shell pwd)

include ${ENVFILE}

IMAGE_NAME       = alpine
IMAGE_VERSION    = 3.10.2
IMAGE_TAG        = $(IMAGE_REGISTRY)/$(IMAGE_REPOSITORY)/$(IMAGE_NAME):$(IMAGE_VERSION)

.DEFAULT_GOAL := build

.PHONY: lint build push

print:: ## Print all the args
	@echo ${IMAGE_TAG}

push:: ## Push the docker image
	@docker push $(IMAGE_TAG)

build: lint ## Build the docker image
	@docker build --pull -t $(IMAGE_TAG) \
		--build-arg MAINTAINER=${MAINTAINER} \
		--build-arg TIMEZONE=${TIMEZONE} \
		$(WORKING_DIR)

lint:: ## Lint dockerfile for best practices
	@hadolint Dockerfile

# A help target including self-documenting targets (see the awk statement)
help: ## This help target
	@echo "Build Docker Image"
	@echo "$$HELP_TEXT"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / \
	{printf "\033[36m%-30s\033[0m  %s\n", $$1, $$2}' $(MAKEFILE_LIST)
