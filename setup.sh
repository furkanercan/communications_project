#!/bin/bash

# Set PYTHONPATH to the 'src' directory relative to the current working directory
export PYTHONPATH=$(pwd)/src:$PYTHONPATH

# Optionally, display the new PYTHONPATH
echo "PYTHONPATH set to: $PYTHONPATH"

        # chmod +x ./setup.sh  # Make sure setup.sh is executable
        # ./setup.sh           # Run the script to set PYTHONPATH

# Set a symbolic link to tests folder
ln -s src tests/src
# Verify the symbolic link
ls -l tests/src