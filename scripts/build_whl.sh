#!/usr/bin/env bash

set -x
set -e
set -u

poetry build -f wheel
