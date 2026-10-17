---
date: 2026-09-30
task: Add a link to github.com/SciScend next to the Blog link on the sciscend.com homepage
written_by: Opus-5.5
---

## Asked
Besides the blog link, put a link to https://github.com/SciScend on sciscend.com.

## Done
- `deploy/placeholder/index.html`: the single `.blog-link` became a `<nav class="links">`
  with `Blog →` and `GitHub →` side by side (flex, wraps on narrow screens).
- Committed (`b2ff17d`), pushed to origin/main.
- Deployed with `npm run deploy:placeholder` (rsync to bulinfo:/var/www/sciscend.com/html/).

## Verified
- Screenshots at 1280 px and 390 px: the two links sit on one row under "Don't Panic!".
- `curl -s https://sciscend.com/` returns the new `<nav class="links">` block
  (Cloudflare: `cf-cache-status: DYNAMIC`, so no purge needed).

## Left open
- The meta description still mentions only the blog; left unchanged.

## Follow-up: pipe instead of arrows
- Asked: drop the arrows, separate the two links with a pipe.
- Now `Blog | GitHub`; the pipe is a muted `<span class="sep" aria-hidden="true">`.
- Committed (`249f162`), pushed, deployed; `curl -s https://sciscend.com/` returns the new markup.

## Follow-up: open in a new tab
- Both links now have `target="_blank" rel="noopener"`.
- Committed (`afb7560`), pushed, deployed; verified with `curl -s https://sciscend.com/`.
