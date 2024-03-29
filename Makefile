PROJECT_ROOT := $(shell pwd)
IMAGE_NAME=tabooword
TAG=1.0.0
HOST_JUPYTER_PORT=8888
DOCKER_CMD_NOTEBOOK=jupyter lab --no-browser
DOCKER_ADDOPTS=\
	-v $(PROJECT_ROOT)/notebook:/workdir/notebook \
	-v $(PROJECT_ROOT)/tabooword:/workdir/tabooword \
	-v $(PROJECT_ROOT)/storage:/workdir/storage \
	--env-file ./env.list \
	$(OPTS)

# build docker image
build:
	docker build dockerfiles -t $(IMAGE_NAME):$(TAG)

# run bash
run_bash:
	docker run -it --rm $(DOCKER_ADDOPTS) $(IMAGE_NAME):$(TAG) bash

run_webapp:
	docker run -d -v $(PROJECT_ROOT)/tabooword/app:/usr/share/nginx/html/ -p 8080:80 --name tabooword-webapp nginx:alpine
run_notebook::
	docker run -d --rm $(DOCKER_ADDOPTS) -p $(HOST_JUPYTER_PORT):8888 --name tabooword-notebook $(IMAGE_NAME):$(TAG) $(DOCKER_CMD_NOTEBOOK)
run_app:
	docker run -d --rm $(DOCKER_ADDOPTS) -p 5000:5000 --name tabooword-app $(IMAGE_NAME):$(TAG) python -m flask run --host=0.0.0.0 --debug
run_notebook::
	@echo "########################################"
	@echo "########################################"
	@echo "##"
	@echo "##  If you run this container locally"
	@echo "##            access jupyter at"
	@echo "##        http://localhost:$(HOST_JUPYTER_PORT)"
	@echo "##"
	@echo "########################################"
	@echo "########################################"
run::
	docker compose up --detach
run::
	@echo "########################################"
	@echo "########################################"
	@echo "##"
	@echo "##  If you run this container locally"
	@echo "##     access web application at at"
	@echo "##       http://localhost:8080"
	@echo "##"
	@echo "########################################"
	@echo "########################################"
	
# remove the container
rm_app:
	docker rm -f tabooword-app || echo
rm_notebook:
	docker rm -f tabooword-notebook || echo


############################ Unittest ############################
test:
	make rm_app
	make run_app
	pytest tests/*

############################ Utility ############################
lint:
	@black .