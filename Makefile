.ONESHELL:
SHELL := /bin/bash
SRC = $(wildcard ./*.ipynb)

all: ipyannotator docs

ipyannotator: $(SRC)
	nbdev_build_lib
	touch ipyannotator

sync:
	nbdev_update_lib

meta:
	python ipyannotator/docs/utils.py

docs: meta
	sphinx-build . ./_build/html -a

quick-docs:
	sphinx-build . ./_build/html -a

test:
	nbdev_test_nbs

release: pypi
	nbdev_conda_package
	nbdev_bump_version

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist
