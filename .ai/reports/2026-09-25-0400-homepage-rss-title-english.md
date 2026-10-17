---
date: 2026-09-25
task: Change the RSS link title on the sciscend.com homepage to English
written_by: Opus-5.5
---

## Asked
Follow-up: the RSS `<link rel="alternate">` title in the homepage head should be English too.

## Done
- `deploy/placeholder/index.html`: title "Блогът на SciScend" changed to "SciScend Blog".
- Committed (`3888b33`), pushed, deployed with `npm run deploy:placeholder`.

## Verified
`curl -s https://sciscend.com/` shows `title="SciScend Blog"` and no Cyrillic "блог" remains on the page.

## Left open
- The feed itself (`/blog/rss.xml`) keeps its Bulgarian title from `src/site.config.ts`; not changed.
