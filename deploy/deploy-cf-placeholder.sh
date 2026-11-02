#!/usr/bin/env bash
#
# Deploy the coming-soon placeholder (deploy/placeholder/) to the Cloudflare
# Worker `sciscend-home` (wrangler.home.jsonc). Nothing to build. Until the route
# is added (migration phase 3), the Worker is reachable only on workers.dev.
#
#   npm run deploy:cf:placeholder
#
# Credentials: as in deploy/deploy-cf.sh.
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
source deploy/cloudflare-env.sh

echo "▶ Deploying deploy/placeholder/ → Worker sciscend-home"
npx wrangler deploy --config wrangler.home.jsonc
