PROJECT_ROOT := $(shell pwd)
IMAGE_NAME=tabooword
TAG=test
HOST_JUPYTER_PORT=8888
DOCKER_CMD_NOTEBOOK=jupyter lab --no-browser
DOCKER_ADDOPTS=\
	-v $(PROJECT_ROOT)/notebook:/workdir/notebook \
	-v $(PROJECT_ROOT)/tabooword:/workdir/tabooword \
	-v $(PROJECT_ROOT)/storage:/workdir/storage \
	-p $(HOST_JUPYTER_PORT):8888 \
	--env-file ./env.list \
	$(OPTS)

# build docker image
build:
	docker build dockerfiles -t $(IMAGE_NAME):$(TAG)

# run bash
run_bash:
	docker run -it --rm $(DOCKER_ADDOPTS) $(IMAGE_NAME):$(TAG) bash

# run notebook
run_notebook::
	docker run -d --rm $(DOCKER_ADDOPTS) --name tabooword-notebook $(IMAGE_NAME):$(TAG) $(DOCKER_CMD_NOTEBOOK)

run_notebook::
	@echo "########################################"
	@echo "########################################"
	@echo "##"
	@echo "##  If you run this container locally:"
	@echo "##            access jupyter at:"
	@echo "##        http://localhost:$(HOST_JUPYTER_PORT)"
	@echo "##"
	@echo "########################################"
	@echo "########################################"

############################ Utility ############################
lint:
	@black .