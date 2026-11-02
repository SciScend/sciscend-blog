#!/usr/bin/env bash
#
# Deploy the blog to the Cloudflare Worker `sciscend-blog` (wrangler.jsonc).
# Builds locally, stages dist/ as dist-cf/blog/, then uploads it with
# `wrangler deploy`. Live on the route sciscend.com/blog/*.
#
#   npm run deploy
#
# Credentials: CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN, from the
# environment or from CLOUDFLARE_ENV_FILE (default: the SciScend workspace's
# .private/cloudflare.env). They are never printed.
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
source deploy/cloudflare-env.sh

echo "▶ Building…"
npm run build

# Stage dist/ under /blog (see the comment in wrangler.jsonc on base_path).
echo "▶ Staging dist/ → dist-cf/blog/"
rm -rf dist-cf
mkdir -p dist-cf/blog
cp -R dist/. dist-cf/blog/
mv dist-cf/blog/_headers dist-cf/_headers
# A public/_redirects (old slug -> new slug) must sit at the assets root too.
if [[ -f dist-cf/blog/_redirects ]]; then mv dist-cf/blog/_redirects dist-cf/_redirects; fi

echo "▶ Deploying dist-cf/ → Worker sciscend-blog"
npx wrangler deploy --config wrangler.jsonc
