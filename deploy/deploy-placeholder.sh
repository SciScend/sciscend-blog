#!/usr/bin/env bash
#
# Deploy the coming-soon placeholder to https://sciscend.com/ (the web root).
# Mirrors deploy/placeholder/ into the html/ folder; the blog lives next to it
# in blog/ and is not touched.
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

[[ -f deploy/deploy.env ]] && source deploy/deploy.env
: "${DEPLOY_SSH:?Set DEPLOY_SSH in deploy/deploy.env}"
: "${PLACEHOLDER_PATH:?Set PLACEHOLDER_PATH in deploy/deploy.env}"
DEPLOY_PORT="${DEPLOY_PORT:-22}"

[[ "$PLACEHOLDER_PATH" == */html ]] || { echo "✗ PLACEHOLDER_PATH must end in /html (got $PLACEHOLDER_PATH)"; exit 1; }

echo "▶ Deploying deploy/placeholder/ → ${DEPLOY_SSH}:${PLACEHOLDER_PATH}/"
rsync -avz --delete -e "ssh -p ${DEPLOY_PORT}" --exclude '.DS_Store' deploy/placeholder/ "${DEPLOY_SSH}:${PLACEHOLDER_PATH}/"

echo "✓ Deployed: https://sciscend.com/"
