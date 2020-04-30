SHELL							:= /bin/bash
WORKING_DIR				:= $(shell pwd)
CONTAINER_BUILDER	:= docker
APP_NAME          := ${IMAGE_NAME}
APP_VERSION       := ${IMAGE_VERSION}


.DEFAULT_GOAL := help

check_defined = \
		$(strip $(foreach 1,$1, \
				$(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
		$(if $(value $1),, \
			$(error Undefined $1$(if $2, ($2))))

.PHONY: build

build:: ## Build image
	$(CONTAINER_BUILDER) build --file ${APP_NAME}/${APP_VERSION}/Dockerfile \
		--build-arg IMAGE_REGISTRY=docker.pkg.github.com/techniumlabs \
		--build-arg IMAGE_REPOSITORY=containers \
	--tag techniumlabs/${IMAGE_NAME}:${IMAGE_VERSION} ${APP_NAME}/${APP_VERSION}

scan:: ## Scan the image
	@trivy --exit-code 0 --severity UNKNOWN,LOW,MEDIUM --no-progress image
	@trivy --exit-code 1 --severity HIGH,CRITICAL --no-progress image

lint:: ## Lint the image
	@hadolint ${APP_NAME}/${APP_VERSION}/Dockerfile

# A help target including self-documenting targets (see the awk statement)
help: ## This help target
	@echo "Build Docker Image"
	@echo "$$HELP_TEXT"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / \
	{printf "\033[36m%-30s\033[0m  %s\n", $$1, $$2}' $(MAKEFILE_LIST)
