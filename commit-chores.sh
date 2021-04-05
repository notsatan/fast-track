#!/bin/bash

# Chores to be executed before every commit. Will be run through a pre-commit
# hook - avoids the need for multiple hooks for these tasks.

# Use poetry to fetch the latest dev requirements and dump them - prevents me from
# having to do this manually, and ensures that I don't end up forgetting this.
poetry export --dev --output requirements-dev.txt

# Likewise, dump normal requirements too.
poetry export --output requirements.txt

# Adding both these files to git staging - will have no effect if there are no changes,
# and if there are any changes, they'll be added to staging and be a part of the next
# commit
git add requirements-dev.txt
git add requirements.txt
