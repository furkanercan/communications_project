#!/bin/bash

# Set PYTHONPATH to the 'src' directory relative to the current working directory
export PYTHONPATH=$(pwd)/src:$PYTHONPATH

# Optionally, display the new PYTHONPATH
echo "PYTHONPATH set to: $PYTHONPATH"