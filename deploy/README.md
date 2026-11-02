# Deploying the SciScend blog

The blog is static. It is built on the laptop and rsynced to the Bullinfo VPS; the
VPS only serves files with nginx, never builds and runs no Node process.

```
laptop                                   Bullinfo VPS (nginx)
──────                                   ─────────────────────────────────────
npm run deploy             ──rsync──►   /var/www/sciscend.com/blog/   → sciscend.com/blog/
npm run deploy:placeholder ──rsync──►   /var/www/sciscend.com/html/   → sciscend.com/
                                                     ▲
                              visitors ── Cloudflare ┘
```

The two trees are siblings, so each `rsync --delete` mirrors only its own folder.
Both scripts refuse to run unless the target ends in `/blog` or `/html`. They
skip `_headers` and `_redirects`, which only the Cloudflare Workers read (see
below).

## One-time local setup

```bash
cp deploy/deploy.env.example deploy/deploy.env   # uses the `bulinfo` SSH alias
```

## Every deploy

```bash
npm run deploy               # blog
npm run deploy:placeholder   # coming-soon page + root robots.txt
```

Verify against the origin, bypassing Cloudflare. The firewall only lets
Cloudflare reach ports 80/443, so run the check on the server itself:

```bash
ssh bulinfo 'curl -sSI --resolve sciscend.com:443:127.0.0.1 https://sciscend.com/blog/'
```

If a change doesn't show publicly, purge the Cloudflare cache
(Caching → Configuration → Purge Everything). HTML is sent with
`must-revalidate`, so this is rare.

## Cloudflare Workers (migration, phase 2)

sciscend.com is moving from the VPS to Cloudflare Workers static assets before
2026-11-12 (decision 021; plan in the workspace,
`operations/cloudflare-workers-migration.md`). This repo has two Workers. For
now they have **no routes**: they run on workers.dev only, and the live site is
still the VPS above. The rsync scripts stay until the VPS is switched off.

| Worker | Config | Command | Assets | workers.dev |
|---|---|---|---|---|
| `sciscend-blog` | `wrangler.jsonc` | `npm run deploy:cf` | `dist/`, staged as `dist-cf/blog/` | <https://sciscend-blog.sciscend.workers.dev/blog/> |
| `sciscend-home` | `wrangler.home.jsonc` | `npm run deploy:cf:placeholder` | `deploy/placeholder/` | <https://sciscend-home.sciscend.workers.dev/> |

```bash
npm run deploy:cf               # build, stage, wrangler deploy (blog)
npm run deploy:cf:placeholder   # wrangler deploy (placeholder, nothing to build)
```

**Credentials.** The scripts need `CLOUDFLARE_ACCOUNT_ID` and
`CLOUDFLARE_API_TOKEN`. If they are not in the environment,
`deploy/cloudflare-env.sh` loads them from `CLOUDFLARE_ENV_FILE` (default: the
workspace's `.private/cloudflare.env`). The token never goes into this repo.

**What replaces nginx.**

| nginx | Workers |
|---|---|
| `try_files $uri $uri/index.html` | `html_handling: auto-trailing-slash`: `/blog/x` answers `307` to `/blog/x/` (nginx served `200` at both) |
| `error_page 404 /blog/404.html` | `not_found_handling: 404-page`: the nearest `404.html`, status 404 |
| security headers | `_headers`, rule `/blog/*` (blog) and `/*` (home) |
| HTML `max-age=0, must-revalidate` | the Workers default, no rule needed |
| `_astro/` 1 year immutable, images and fonts 30 days, `robots.txt`, `llms.txt`, `rss.xml` 1 hour | `_headers` |
| content types of `llms.txt`, `rss.xml` | `_headers` (Workers would send `text/plain` without a charset and `application/xml`) |
| `/blog`, `/ivapopova`, `/ivapopova/projects`, `/ivapopova/cv` 301 | `deploy/placeholder/_redirects` on `sciscend-home`: these paths fall outside the `.../blog/*` and `.../ivapopova/*` routes |
| `www` -> apex, gzip, TLS | Cloudflare zone (phase 3), automatic |

Things that are easy to get wrong in `_headers`:

- Paths are the public ones, with `/blog` in front.
- Every matching rule adds its headers, and the same header from two rules is
  joined with a comma. An image under `_astro/` matches both the `_astro` rule and
  an image rule, so the `_astro` rule starts with `! Cache-Control` to drop the
  other one.
- `_headers` cannot match by status: a 404 under `_astro/` or for a missing image
  gets the long `Cache-Control` too (nginx sent it only with 2xx and 3xx).

**Why the blog is staged in `dist-cf/`.** The plan was `"directory": "./dist"`
with `"base_path": "/blog"`. On 2026-11-03 Cloudflare refused it: `A non-root
assets.base_path is not enabled for this account. [code: 100343]`. So
`deploy/deploy-cf.sh` copies `dist/` to `dist-cf/blog/` and moves `_headers` to
`dist-cf/`, and the asset paths carry `/blog` themselves. If `base_path` is
enabled for the account later, set `directory: ./dist` and `base_path: /blog`
and drop the staging step; `_headers` stays the same. `dist-cf/` is gitignored.

**Check after a deploy** (headers and content types):

```bash
B=https://sciscend-blog.sciscend.workers.dev
for p in /blog/ /blog/tag/ai-agents/ /blog/rss.xml /blog/sitemap-index.xml /blog/llms.txt /blog/no-such-page/; do
  echo "== $p"; curl -sI "$B$p" | grep -iE '^(HTTP|content-type|cache-control|location|x-frame-options)'
done
```

**Phase 3 (switch the live domain)** is adding `routes` to the two configs
(`sciscend.com/blog/*` for the blog, `sciscend.com/*` for home, home last) plus
the `www` Redirect Rule in the zone. See the plan in the workspace.

## Changing nginx

`nginx-sciscend.conf` in this folder is the source of truth for the live site
config (moved here from `sciscend-web` on 2026-09-22). Edit it here, then:

```bash
scp deploy/nginx-sciscend.conf bulinfo:/tmp/sciscend.conf
ssh bulinfo 'sudo cp /etc/nginx/sites-available/sciscend.com /etc/nginx/sites-available/sciscend.com.bak-$(date +%F) \
  && sudo cp /tmp/sciscend.conf /etc/nginx/sites-available/sciscend.com \
  && sudo nginx -t && sudo systemctl reload nginx'
```

`nginx -t` before the reload means a bad config never takes the site down; if it
fails, copy the backup back.

## Server facts

| Thing | Value |
|---|---|
| SSH | `bulinfo` alias in `~/.ssh/config` |
| Web roots | `/var/www/sciscend.com/html` (placeholder), `/var/www/sciscend.com/blog` (blog), owned by `ubuntu` — no sudo for deploys |
| nginx site | `/etc/nginx/sites-available/sciscend.com` |
| TLS | Let's Encrypt, cert `sciscend.com` (apex + `www`), certbot systemd timer |
| DNS | Cloudflare, proxied |
| Firewall | ufw: SSH open (keys only); 80/443 only from Cloudflare's IP ranges. Runbook in the workspace's `operations/hosting-and-deployment.md` |

Rebuilding the server from scratch is documented in the workspace:
`operations/hosting-and-deployment.md`.
