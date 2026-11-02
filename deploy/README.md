# Deploying the SciScend blog

The blog and the coming-soon page at `/` are static. They are built on the
laptop and uploaded with `wrangler deploy` to two Cloudflare Workers that serve
static assets only, no code. Since 2026-11-03 they serve the live site
(decision 021 in the workspace; migration plan:
`operations/cloudflare-workers-migration.md`).

```
laptop                                        Cloudflare (zone sciscend.com)
------                                        ------------------------------
npm run deploy             --wrangler-->  Worker sciscend-blog   route sciscend.com/blog/*
npm run deploy:placeholder --wrangler-->  Worker sciscend-home   route sciscend.com/*
(workspace) bin/build-portfolio.py --deploy-cf  Worker sciscend-portfolio  route sciscend.com/ivapopova/*
```

The most specific route wins, so `/blog/...` goes to the blog and everything
without its own Worker goes to `sciscend-home`. Each deploy replaces only its own
Worker.

| Worker | Config | Command | Assets |
|---|---|---|---|
| `sciscend-blog` | `wrangler.jsonc` | `npm run deploy` | `dist/`, staged as `dist-cf/blog/` |
| `sciscend-home` | `wrangler.home.jsonc` | `npm run deploy:placeholder` | `deploy/placeholder/` |

`workers_dev` and `preview_urls` are off: the site exists only on sciscend.com.

## Credentials

The scripts need `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_API_TOKEN`. If they are
not in the environment, `deploy/cloudflare-env.sh` loads them from
`CLOUDFLARE_ENV_FILE` (default: the workspace's `.private/cloudflare.env`). The
token (template "Edit Cloudflare Workers", account + zone sciscend.com) never
goes into this repo. Check: `npx wrangler whoami` with the variables loaded.

## Every deploy

```bash
npm run deploy               # build, stage dist-cf/, wrangler deploy (blog)
npm run deploy:placeholder   # wrangler deploy (placeholder, nothing to build)
```

Check after a deploy:

```bash
for p in /blog/ /blog/tag/ai-agents/ /blog/rss.xml /blog/sitemap-index.xml /blog/llms.txt /blog/no-such-page/; do
  echo "== $p"; curl -sI "https://sciscend.com$p" | grep -iE '^(HTTP|content-type|cache-control|location)'
done
```

HTML is sent with `max-age=0, must-revalidate`, so a deploy shows at once. If it
does not, purge the cache (dashboard -> sciscend.com -> Caching -> Configuration
-> Purge Everything).

## Redirects (renamed slugs and tags)

A renamed post or tag needs a 301 from the old URL. Put it in
`public/_redirects` with the full public paths:

```
/blog/old-slug/   /blog/new-slug/   301
```

`deploy/deploy.sh` moves the file to the assets root. Limit: 2,000 static
redirects. `/blog` -> `/blog/` itself lives in `deploy/placeholder/_redirects`,
because `/blog` without the slash is outside the blog route.

## Headers and other rules

| Need | Where |
|---|---|
| `/blog/x` -> `/blog/x/` | `html_handling: auto-trailing-slash` (307) |
| 404 page | `not_found_handling: 404-page`: the nearest `404.html`, status 404 |
| security headers, cache times, content types, HTML charset | `public/_headers` (blog), `deploy/placeholder/_headers` (home) |
| `www` -> apex, HTTP -> HTTPS, TLS, compression | Cloudflare zone settings (workspace: `operations/hosting-and-deployment.md`) |

Things that are easy to get wrong in `_headers`:

- Paths are the public ones, with `/blog` in front.
- Every matching rule adds its headers, and the same header from two rules is
  joined with a comma. An image under `_astro/` matches both the `_astro` rule and
  an image rule, so the `_astro` rule starts with `! Cache-Control` to drop the
  other one.
- `_headers` cannot match by status: a 404 under `_astro/` or for a missing image
  gets the long `Cache-Control` too.
- Limit: 100 rules.

## Why the blog is staged in `dist-cf/`

The plan was `"directory": "./dist"` with `"base_path": "/blog"`. On 2026-11-03
Cloudflare refused it: `A non-root assets.base_path is not enabled for this
account. [code: 100343]`. So `deploy/deploy.sh` copies `dist/` to
`dist-cf/blog/` and moves `_headers` (and `_redirects`) to `dist-cf/`; the asset
paths carry `/blog` themselves. If `base_path` is enabled for the account later,
set `directory: ./dist` and `base_path: /blog` and drop the staging step;
`_headers` stays the same. `dist-cf/` is gitignored.

## Rollback

Until the Bullinfo VPS expires (2026-11-12), the old nginx site still holds the
2026-11-03 content: removing the routes (dashboard -> Workers & Pages -> Worker
-> Settings -> Domains & Routes) sends the requests back to it. After that date,
roll back by deploying an older commit. The former rsync scripts and nginx config
are in git history (removed in the commit "Deploy to Cloudflare Workers only").
