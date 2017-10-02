all: test

VERSION = `cat version.txt | xargs`

PACKAGE = dockerman
IMAGE = mbodenhamer/${PACKAGE}-dev
PYDEV = docker run --rm -it -e BE_UID=`id -u` -e BE_GID=`id -g` \
	-v /var/run/docker.sock:/var/run/docker.sock -v $(CURDIR):/app $(IMAGE)
VERSIONS = 2.7.14,3.6.2

#-------------------------------------------------------------------------------
# Docker image management

docker-build:
	@docker build -t $(IMAGE):latest --build-arg versions=$(VERSIONS) .

docker-first-build:
	@docker build -t $(IMAGE):latest --build-arg versions=$(VERSIONS) \
	--build-arg reqs=requirements.yml .
	@$(PYDEV) depman export dev -t pip -o dev-requirements.in --no-header
	@$(PYDEV) depman export prod -t pip -o requirements.in --no-header
	@$(PYDEV) pip-compile dev-requirements.in
	@$(PYDEV) pip-compile requirements.in

docker-rmi:
	@docker rmi $(IMAGE)

docker-push:
	@docker push ${IMAGE}:latest

docker-pull:
	@docker pull ${IMAGE}:latest

docker-shell:
	@$(PYDEV) bash

.PHONY: docker-build docker-first-build docker-rmi docker-push docker-pull \
	docker-shell
#-------------------------------------------------------------------------------
# Build management

check:
	@$(PYDEV) check-manifest

build: check
	@$(PYDEV) python setup.py sdist bdist_wheel

.PHONY: check build
#-------------------------------------------------------------------------------
# Documentation

docs:
	@$(PYDEV) sphinx-apidoc -f -o docs/ ${PACKAGE}/
	@$(PYDEV) make -C docs html

view:
	@python -c "import webbrowser as wb; \
	wb.open('docs/_build/html/index.html')"

.PHONY: docs view
#-------------------------------------------------------------------------------
# Dependency management

pip-compile:
	@$(PYDEV) pip-compile dev-requirements.in
	@$(PYDEV) pip-compile requirements.in

.PHONY: pip-compile
#-------------------------------------------------------------------------------
# Tests

test:
	@$(PYDEV) coverage erase
	@$(PYDEV) tox
	@$(PYDEV) coverage html

quick-test:
	@$(PYDEV) nosetests -v --pdb --pdb-failures

dist-test: build
	@$(PYDEV) dist-test $(VERSION)

show:
	@python -c "import webbrowser as wb; wb.open('htmlcov/index.html')"

.PHONY: test quick-test dist-test show
#-------------------------------------------------------------------------------
# Cleanup

clean:
	@$(PYDEV) fmap -r ${PACKAGE} 'rm -f' '*.py[co]'
	@$(PYDEV) fmap -r ${PACKAGE} -d rmdir __pycache__
	@$(PYDEV) fmap -r tests 'rm -f' '*.py[co]'
	@$(PYDEV) fmap -r tests -d rmdir __pycache__
	@$(PYDEV) make -C docs clean

.PHONY: clean
#-------------------------------------------------------------------------------
