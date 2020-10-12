#!/bin/bash

jupyter notebook stop
nohup jupyter lab --ip=0.0.0.0 --no-browser --allow-root &
