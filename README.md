```sh
# Install deps
uv sync

# Download and post-process fund category proposals
# Change X-CSRF-TOKEN value in download script with a value
# that you would get from running the for examples the "challenges" API end point
# https://www.lidonation.com/catalyst-explorer/api#/challenge/challenges
uv run download_proposals.py
uv run process_proposals.py

# Classify proposals
uv run classify.py
```
