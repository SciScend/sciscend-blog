#!/usr/bin/env bash
#
# Deploy the blog to https://sciscend.com/blog/.
# Builds locally (the 1 GB VPS never builds), then mirrors dist/ into the blog
# web root. Only that folder is touched — the placeholder at / is separate.
#
#   cp deploy/deploy.env.example deploy/deploy.env   # once
#   npm run deploy
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

[[ -f deploy/deploy.env ]] && source deploy/deploy.env
: "${DEPLOY_SSH:?Set DEPLOY_SSH in deploy/deploy.env}"
: "${DEPLOY_PATH:?Set DEPLOY_PATH in deploy/deploy.env}"
DEPLOY_PORT="${DEPLOY_PORT:-22}"

# Guard against a typo that would mirror the blog over the placeholder.
[[ "$DEPLOY_PATH" == */blog ]] || { echo "✗ DEPLOY_PATH must end in /blog (got $DEPLOY_PATH)"; exit 1; }

echo "▶ Building…"
npm run build

echo "▶ Deploying dist/ → ${DEPLOY_SSH}:${DEPLOY_PATH}/"
ssh -p "$DEPLOY_PORT" "$DEPLOY_SSH" "mkdir -p '$DEPLOY_PATH'"
rsync -avz --delete -e "ssh -p ${DEPLOY_PORT}" --exclude '.DS_Store' dist/ "${DEPLOY_SSH}:${DEPLOY_PATH}/"

echo "✓ Deployed: https://sciscend.com/blog/"
