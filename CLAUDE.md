# sciscend-blog

The blog at https://sciscend.com/blog/. Read `docs/tech-spec.md` before changing
structure, URLs, the schema, nginx or deploy. Company facts live in the SciScend
workspace (`/data/projects/SciScend`), not here.

## Rules

- **Posts** are written and published with the `/new-post` skill. Iva's voice and
  opinions only — never invent results, numbers or quotes.
- **Bulgarian by default**; technical terms stay in English (pipeline, prompt,
  fine-tuning — no literal translations). English posts go under `research/`.
- **Tags**: run `npm run tags` and reuse; lowercase kebab-case, English.
- **Slugs and tag names are permanent URLs.** Don't rename a published one
  without adding an nginx 301 in `deploy/nginx-sciscend.conf`.
- **Public wording**: "SciScend", never "SciScend ЕООД". Never "д-р", "PhD" or
  "доктор" for Iva — the approved author text is in `src/site.config.ts`.
- **Private data**: every post passes the workspace's
  `bin/redact-private-data.py --dry-run` and the `check-private-data` reading pass
  before publishing. No server IPs, paths or account details in posts.
- **Deploy** only with `npm run deploy` / `npm run deploy:placeholder`. Never build
  on the VPS. `deploy/nginx-sciscend.conf` is the live nginx config — edit here,
  then follow `deploy/README.md`.
- After a finished task: commit with a short message and push.
