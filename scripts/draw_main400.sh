#!/usr/bin/env bash
# Long draw: paced and very patient, because OpenAlex list-query cooldowns run for
# hours. Checkpoints after every accepted pair (data/samples/main400.partial.json).
set -u
cd "$(dirname "$0")/.."
export OPENALEX_PACE="${OPENALEX_PACE:-1.5}"
export OPENALEX_PATIENCE="${OPENALEX_PATIENCE:-$(python3 -c "print(','.join(['900']*24))")}"
exec uv run python -m genesis.sample --pairs 400 --holdout 60 --out data/samples/main400.json
