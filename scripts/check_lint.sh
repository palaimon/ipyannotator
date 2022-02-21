#!/usr/bin/env bash

echo "Runnig Flake8 on nbs"

# E402 -> Module level import not at top of file
# Cause : We might use some imports for testing inside the nbs.
# F401 -> Module imported but unused
# F403 -> 'from module import *' used; unable to detect undefined names
# F405 -> Name may be undefined, or defined from star imports: module
# Cause : "from nbdev import *"
FLAKE=$(poetry run nbqa flake8 --ignore=E402,F401,F403,F405,E265,W504 nbs/)

if [[ -n "${FLAKE// }" ]]; then
	echo "Some error where found in flake8"
	poetry run nbqa flake8 --ignore=E402,F401,F403,F405,E265,W504 nbs/
	false
	exit 1
fi

echo "Runnig Flake8 on generated library"

FLAKE=$(poetry run flake8 ipyannotator)

if [[ -n "$FLAKE" ]]; then
	echo "Some error where found in flake8 running on generated library"
	poetry run flake8 ipyannotator
	false
	exit 1;
fi

echo "Running pylint"

PYLINT=$(poetry run pylint ./ipyannotator --rcfile=.pylintrc)

# pylint will return the grade of the code. To make sure the lines with the grade don't
# make the test fail, we make the test pass if the output is equals to 3 lines.
if [[ ! $(wc -l <<< "$PYLINT") = "3" ]]; then
	echo "Pylint found some error!"
	poetry run pylint ./ipyannotator --rcfile=.pylintrc
	false
	exit 1;
fi

echo "Running MYPY on notebooks"

MYPY=$(poetry run nbqa mypy --config-file=pyproject.toml nbs --ignore-missing-imports)


# Will only works if the output is different then one line
# This happens because mypy will always return one line if the tests sucess
# Line example: Success: no issues found in 3 source files
if [[ ! $(wc -l <<< "$MYPY") = "1" ]]; then
	echo "Mypy found some error!"
	poetry run nbqa mypy --config-file=pyproject.toml nbs --ignore-missing-imports
	exit 1;
fi

