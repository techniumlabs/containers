SHELL					:= /bin/bash
WORKING_DIR   := $(shell pwd)
REGISTRY_USER :=
REGISTRY_PASS :=

include config

.DEFAULT_GOAL := help

.PHONY: login

login:: ## Login to docker Registry
	@docker login -u $(REGISTRY_USER) -p $(REGISTRY_PASS) $(IMAGE_REGISTRY)

lint-%:: ## Lint image
	$(MAKE) -C $* ENVFILE=$(PWD)/config lint

build-%:: ## Build image
	$(MAKE) -C $* ENVFILE=$(PWD)/config build

release-%:: login ## Release image
	$(MAKE) -C $* ENVFILE=$(PWD)/config release

help-%:: ## Release image
	$(MAKE) -C $* ENVFILE=$(PWD)/config help

# A help target including self-documenting targets (see the awk statement)
help: ## This help target
	@echo "Build Docker Image"
	@echo "$$HELP_TEXT"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / \
	{printf "\033[36m%-30s\033[0m  %s\n", $$1, $$2}' $(MAKEFILE_LIST)
