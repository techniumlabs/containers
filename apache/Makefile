SHELL					:= /bin/bash
WORKING_DIR   := $(shell pwd)

include ${ENVFILE}

IMAGE_NAME       = apache
IMAGE_VERSION    = alpine-3.10.2
BRANCH	:=$(shell git rev-parse --abbrev-ref HEAD)
ifeq ($(BRANCH),master)
	# If the branch is 'master'.
	BUILD_SUFFIX =
else
	# Else set the image version to 'latest' and use the 'snapshots' prefix in S3.
	BUILD_SUFFIX     = -dev-$(shell git log -1 --pretty=format:"%H")
endif

IMAGE_TAG        = $(IMAGE_REGISTRY)/$(IMAGE_REPOSITORY)/$(IMAGE_NAME):$(IMAGE_VERSION)$(BUILD_SUFFIX)

.DEFAULT_GOAL := release

.PHONY: lint build push

push:: ## Push the docker image
	@docker push $(IMAGE_TAG)

build: lint ## Build the docker image
	@docker build --pull -t $(IMAGE_TAG) \
		--build-arg IMAGE_REGISTRY=${IMAGE_REGISTRY} \
		--build-arg IMAGE_REPOSITORY=${IMAGE_REPOSITORY} \
		$(WORKING_DIR)

release: build push

lint:: ## Lint dockerfile for best practices
	@hadolint Dockerfile

# A help target including self-documenting targets (see the awk statement)
help: ## This help target
	@echo "Build Alpine Docker Image"
	@echo "$$HELP_TEXT"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / \
	{printf "\033[36m%-30s\033[0m  %s\n", $$1, $$2}' $(MAKEFILE_LIST)
