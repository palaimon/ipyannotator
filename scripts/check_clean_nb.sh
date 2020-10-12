#!/usr/bin/env bash

set -x

poetry install

poetry run nbdev_clean_nbs

MODIFIED=$(git status -uno -s | grep '.*\.ipynb')

if [ -n "$MODIFIED" ]; then
  echo "!! ::error:: Detected notebooks that are not cleaned."
  echo "List of notebooks that are not clean:"
  git status -uno -s | grep '.*\.ipynb'
  false;
fi
