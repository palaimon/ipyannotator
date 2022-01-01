#!/usr/bin/env bash

# This will build the lib from the notebooks
poetry run nbdev_build_lib

out=$(git status -uno -s | grep '.*\.py')

# Check if the string is null/empty
if [ -n "$out" ]; then 
    echo -e "!!! ::error:: Detected difference between the notebooks and the library";
    echo $out;
    false;
fi
