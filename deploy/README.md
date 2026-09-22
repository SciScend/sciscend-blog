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
Both scripts refuse to run unless the target ends in `/blog` or `/html`.

## One-time local setup

```bash
cp deploy/deploy.env.example deploy/deploy.env   # uses the `bulinfo` SSH alias
```

## Every deploy

```bash
npm run deploy               # blog
npm run deploy:placeholder   # coming-soon page + root robots.txt
```

Verify against the origin, bypassing Cloudflare:

```bash
curl -sSI --resolve sciscend.com:443:<VPS-IP> https://sciscend.com/blog/
```

If a change doesn't show publicly, purge the Cloudflare cache
(Caching → Configuration → Purge Everything). HTML is sent with
`must-revalidate`, so this is rare.

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

Rebuilding the server from scratch is documented in the workspace:
`operations/hosting-and-deployment.md`.
