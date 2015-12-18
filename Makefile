.PHONY: all buildout tests publish

SETUPTOOLS_VERSION = "19.0"
BOOTSTRAP_BUILDOUT = "https://bootstrap.pypa.io/bootstrap-buildout.py"

all:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

buildout: ## Setup development environment
	@rm bootstrap-buildout.py -f
	@rm buildout -rf
	@wget $(BOOTSTRAP_BUILDOUT)
	@for v in 2 3; do \
		mkdir -p buildout/$$v;\
		python$$v bootstrap-buildout.py -c py$$v.cfg --setuptools-version=$(SETUPTOOLS_VERSION);\
		buildout/$$v/bin/buildout -c py$$v.cfg;\
		rm .installed.cfg;\
	done
	@rm bootstrap-buildout.py

tests:    ## Run tests
	@for v in `ls buildout`; do \
		echo Python $$v;\
		buildout/$$v/bin/coverage run --source mediator.py setup.py test -q && buildout/$$v/bin/coverage report -m;\
		echo;\
	done
	@rm __pycache__ -r
	@rm mediator.pyc tests.pyc stubs.pyc
	@rm mediator.egg-info -r
	@rm .coverage

publish:  ## Upload package to PyPI
	@python setup.py sdist upload
