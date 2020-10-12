#!/usr/bin/env bash

set -x
set -e
set -u

poetry install
poetry run nbdev_test_nbs
