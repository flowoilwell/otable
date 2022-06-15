SHELL := bash
.SHELLFLAGS := -eux -o pipefail -c
.DEFAULT_GOAL := build
.DELETE_ON_ERROR:  # If a recipe to build a file exits with an error, delete the file.
.SUFFIXES:  # Remove the default suffixes which are for compiling C projects.
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

export PIP_DISABLE_PIP_VERSION_CHECK=1
pip-install := ve/bin/pip --no-input install --constraint constraints.txt
pip-check := ve/bin/pip show -q

source_code := src

isort := ve/bin/isort --multi-line=VERTICAL_HANGING_INDENT --trailing-comma --no-sections

########################################################################################
# Build targets
#
# It is acceptable for other targets to implicitly depend on these targets having been
# run.  I.e., it is ok if "make lint" generates an error before "make" has been run.

.PHONY: build
build: ve development-utilities install-flake8-plugins

.PHONY: install-flake8-plugins
install-flake8-plugins:
	$(pip-install) flake8-docstrings

ve:
	python3.10 -m venv ve
	$(pip-install) -e .

ve/bin/%:
	# Install development utility "$*"
	$(pip-install) $*

# Utilities we use during development.
.PHONY: development-utilities
development-utilities: ve/bin/black
development-utilities: ve/bin/coverage
development-utilities: ve/bin/flake8
development-utilities: ve/bin/isort
development-utilities: ve/bin/mypy
development-utilities: ve/bin/pylint

########################################################################################
# Test and lint targets

.PHONY: pylint
pylint:
	ve/bin/pylint $(source_code) --output-format=colorized

.PHONY: flake8
flake8:
	ve/bin/flake8 $(source_code) tests \
	    --docstring-convention=all --extend-ignore=D105,D203,D213,D413,D407,D400

.PHONY: mypy
mypy:
	ve/bin/mypy $(source_code) --strict
	ve/bin/mypy tests/

.PHONY: black-check
black-check:
	ve/bin/black -S $(source_code) tests --check

.PHONY: isort-check
isort-check:
	$(isort) $(source_code) tests --diff --check

.PHONY: lint
lint: mypy flake8 black-check isort-check pylint

.PHONY: unittest
unittest:
	ve/bin/python -m unittest

.PHONY: doctest
doctest:
	ve/bin/python -m tests.doctest

.PHONY: coverage
coverage:
	ve/bin/coverage run --branch -m unittest
	ve/bin/coverage run --branch --append -m tests.doctest
	PYTHONWARNINGS=ignore ve/bin/coverage report --ignore-errors --fail-under=100 --show-missing --skip-empty

.PHONY: test
test: unittest doctest

.PHONY: check
check: test lint coverage
	@echo 'All checks passed!'

########################################################################################
# Automated fixers

.PHONY: black
black:
	ve/bin/black -S $(source_code) tests

.PHONY: isort
isort:
	$(isort) $(source_code) tests

########################################################################################
# Cleanup targets

.PHONY: clean-%
clean-%:
	rm -rf $*

.PHONY: clean-pycache
clean-pycache:
	find . -name __pycache__ -delete

.PHONY: clean
clean: clean-ve clean-pycache
