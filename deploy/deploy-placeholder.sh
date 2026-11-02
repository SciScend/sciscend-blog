#!/usr/bin/env bash
#
# Deploy the coming-soon placeholder (deploy/placeholder/) to the Cloudflare
# Worker `sciscend-home` (wrangler.home.jsonc). Nothing to build. Live on the
# route sciscend.com/* (every path without a more specific route).
#
#   npm run deploy:placeholder
#
# Credentials: as in deploy/deploy.sh.
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
source deploy/cloudflare-env.sh

echo "▶ Deploying deploy/placeholder/ → Worker sciscend-home"
npx wrangler deploy --config wrangler.home.jsonc
