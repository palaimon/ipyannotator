#!/usr/bin/env bash

out=$(poetry -q run nbdev_diff_nbs)

echo "DIFF LEN="${#out}

if [ ${#out} -gt 0 ]; then 
    echo -e "!!! ::error:: Detected difference between the notebooks and the library";
    echo $out;
    false;
fi
