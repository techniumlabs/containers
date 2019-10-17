SHELL						 := /bin/bash
WORKING_DIR      := $(shell pwd)
IMAGE_NAME       := base
IMAGE_VERSION    := alpine-3.10.2-r0
BRANCH					 :=$(shell git rev-parse --abbrev-ref HEAD)

include ${ENVFILE}

ifeq ($(BRANCH),master)
	# If the branch is 'master'.
	BUILD_SUFFIX =
else
	# Else set the image version to 'latest' and use the 'snapshots' prefix in S3.
	BUILD_SUFFIX     = -dev-$(shell git log -1 --pretty=format:"%H")
endif

check_defined = \
		$(strip $(foreach 1,$1, \
				$(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
		$(if $(value $1),, \
			$(error Undefined $1$(if $2, ($2))))

$(call check_defined, IMAGE_REGISTRY, Registry url)
$(call check_defined, IMAGE_REPOSITORY, Repository name)

ifeq ($(IMAGE_REGISTRY),hub.docker.com)
	IMAGE_TAG = $(IMAGE_REPOSITORY)/$(IMAGE_NAME):$(IMAGE_VERSION)$(BUILD_SUFFIX)
else
	IMAGE_TAG = $(IMAGE_REGISTRY)/$(IMAGE_REPOSITORY)/$(IMAGE_NAME):$(IMAGE_VERSION)$(BUILD_SUFFIX)
endif

.DEFAULT_GOAL := release

.PHONY: lint build push

release: build push

lint:: ## Lint dockerfile for best practices
	@hadolint Dockerfile

push:: ## Push the docker image
	@docker push $(IMAGE_TAG)

build: lint ## Build the docker image
	@docker build --pull -t $(IMAGE_TAG) \
		--build-arg MAINTAINER=${MAINTAINER} \
		--build-arg TIMEZONE=${TIMEZONE} \
		$(WORKING_DIR)

# A help target including self-documenting targets (see the awk statement)
help: ## This help target
	@echo "Build Alpine Docker Image"
	@echo "$$HELP_TEXT"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / \
	{printf "\033[36m%-30s\033[0m  %s\n", $$1, $$2}' $(MAKEFILE_LIST)
