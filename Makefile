SHELL					:= /bin/bash
WORKING_DIR   := $(shell pwd)

.DEFAULT_GOAL := build

.PHONY: build

alpine:: ## Build alpine image
	$(MAKE) -C alpine ENVFILE=$(PWD)/config

php:: ## Build php image
	$(MAKE) -C php ENVFILE=$(PWD)/config

# A help target including self-documenting targets (see the awk statement)
help: ## This help target
	@echo "Build Docker Image"
	@echo "$$HELP_TEXT"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / \
	{printf "\033[36m%-30s\033[0m  %s\n", $$1, $$2}' $(MAKEFILE_LIST)
