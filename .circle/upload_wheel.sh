#!/bin/bash

set -x

# Get the range of commits from the latest merge commit
COMMIT_RANGE=$(git log --merges --max-count 1 | grep ^Merge | grep -ow "[a-z0-9]\{7\}" | xargs | sed -e 's/ /../g')

# Check the diff in that commit range and see if there are any version changes
CHANGES=$(git diff -U0 "$COMMIT_RANGE" -- setup.py | grep -c version)

# If we have modified the version, we'll have two lines
if [ "$CHANGES" -eq 2 ]
then
  devpi login $$PYPI_USERNAMWE --password $PYPI_PASSWORD
  devpi upload --formats bdist_wheel
fi
