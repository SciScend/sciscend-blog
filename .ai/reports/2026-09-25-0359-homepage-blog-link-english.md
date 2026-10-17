---
date: 2026-09-25
task: Change the "Блог" link on the sciscend.com homepage to English, push and deploy
written_by: Opus-5.5
---

## Asked
The homepage at sciscend.com showed "Блог"; change it to English, push and deploy.

## Done
- `deploy/placeholder/index.html`: link text `Блог →` changed to `Blog →`.
- Committed (`19d6c4e`), pushed to origin/main.
- Deployed with `npm run deploy:placeholder` (rsync to bulinfo:/var/www/sciscend.com/html/).

## Verified
`curl -s https://sciscend.com/` now returns `<a class="blog-link" href="/blog/">Blog →</a>`.

## Left open
- The RSS `<link rel="alternate">` title in the page head is still "Блогът на SciScend"
  (not visible on the page; it matches the Bulgarian blog's own feed title), left unchanged.
