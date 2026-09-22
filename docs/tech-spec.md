---
title: SciScend blog — technical specification
status: implemented (v0.1, live 2026-09-22)
written_by: Opus-5.5
---

# SciScend blog — technical specification

The blog at **https://sciscend.com/blog/**: Bulgarian-first articles on practical AI,
Python and machine learning — model tests, beginner guides, AI for small business.
This document is the source of truth for how it is built, served and published.
Why it exists in this form is recorded in the SciScend workspace,
`history/decisions/010-standalone-blog-at-sciscend-com-blog.md`.

## 1. Scope

| In scope | Out of scope (for now) |
|---|---|
| Article list, article pages, tag (category) pages | The company website — `sciscend-web` is on hold and will be redone |
| RSS, sitemap, `llms.txt`, JSON-LD, Open Graph | Comments, newsletter, search, analytics |
| Bulgarian posts; English posts under `/blog/research/` | `hreflang` pairs (added with the first translated post) |
| The coming-soon placeholder at `/` and the nginx config | The "Building SciScend" series — stays in the workspace, published later |

## 2. Requirements

1. **URL:** the blog lives at `sciscend.com/blog/`, a subdirectory rather than a
   subdomain, so links to posts build authority for the whole domain and the
   URLs survive the future website unchanged.
2. **The homepage stays the placeholder.** Blog deploys never touch it and
   placeholder deploys never touch the blog.
3. **Language:** UI in Bulgarian. Each post declares its own `lang` (`bg` default,
   `en` allowed). Technical terms stay in English in Bulgarian text.
4. **Categories are not predefined.** They are the tags posts carry; every tag in
   use gets a page. Tags are written into the post (by the agent that drafts it,
   approved by Iva) — never generated at build time, so category URLs are stable.
5. **Drafts** never reach production.
6. **Minimal design** in the brand colours, readable on a phone, light and dark.
7. **Static only.** The 1 GB VPS serves files; it never builds and runs no Node.

## 3. Stack

| Part | Choice |
|---|---|
| Generator | Astro 7, static output, `@astrojs/mdx` |
| Feeds / SEO | `@astrojs/rss`, `@astrojs/sitemap`, hand-written JSON-LD and `llms.txt` |
| Styling | one hand-written stylesheet, `src/styles/global.css` — no framework |
| Fonts | system font stack (Cyrillic-complete, zero requests) |
| Code highlighting | Shiki, dual theme (`github-light` / `github-dark`) |
| Hosting | Bullinfo VPS, nginx 1.24, behind Cloudflare (proxied) |
| Repo | `github.com/SciScend/sciscend-blog` (private), local `/data/projects/sciscend-blog` |

Key `astro.config.mjs` settings: `site: 'https://sciscend.com'`, `base: '/blog'`,
`trailingSlash: 'always'`, `build.format: 'directory'`. The build output in `dist/`
is *unprefixed* (`dist/index.html`, `dist/tag/…`); the prefix comes from where it
is deployed (`/var/www/sciscend.com/blog/`).

## 4. Repository layout

```
sciscend-blog/
├── astro.config.mjs
├── src/
│   ├── site.config.ts          all blog metadata: title, description, author, url()/asset() helpers
│   ├── content.config.ts       the post schema (see §5)
│   ├── content/blog/           the posts — the file path is the URL
│   ├── lib/posts.ts            getPosts() (drafts only in dev), tagCounts(), dates, reading time
│   ├── lib/schema.ts           JSON-LD: Blog, BlogPosting, Person, Organization
│   ├── layouts/BaseLayout.astro  <head> (meta, canonical, OG, RSS, JSON-LD), header, footer
│   ├── components/PostList.astro
│   ├── styles/global.css
│   └── pages/
│       ├── index.astro         /blog/
│       ├── [...slug].astro     /blog/<slug>/  and  /blog/research/<slug>/
│       ├── tag/index.astro     /blog/tag/            all tags with counts
│       ├── tag/[tag].astro     /blog/tag/<tag>/
│       ├── rss.xml.ts          /blog/rss.xml
│       ├── llms.txt.ts         /blog/llms.txt
│       └── 404.astro           /blog/404.html
├── public/                     logo, favicons, default share image, post images
├── scripts/tags.mjs            `npm run tags` — tags in use with counts
├── deploy/
│   ├── deploy.sh               `npm run deploy`
│   ├── deploy-placeholder.sh   `npm run deploy:placeholder`
│   ├── deploy.env.example      copy to deploy.env (gitignored)
│   ├── nginx-sciscend.conf     the live nginx site config — source of truth
│   ├── placeholder/            the coming-soon page + root robots.txt
│   └── README.md               runbook
├── .claude/skills/new-post/    /new-post — draft, check, publish, LinkedIn text
└── docs/tech-spec.md           this file
```

## 5. Content model

One Markdown/MDX file per post in `src/content/blog/`. The path is the URL:

| File | URL |
|---|---|
| `src/content/blog/jev-na-balgarski.md` | `/blog/jev-na-balgarski/` |
| `src/content/blog/research/foo.md` | `/blog/research/foo/` |

Slugs are Latin, kebab-case, transliterated, without a date; a slug is a permanent
URL and is chosen once.

Frontmatter (validated by `src/content.config.ts`; a violation fails the build):

| Field | Type | Required | Notes |
|---|---|---|---|
| `title` | string | yes | ≤ 70 characters recommended |
| `description` | string | yes | 120–160 characters; meta description, OG, RSS, listing |
| `pubDate` | date | yes | |
| `updatedDate` | date | no | set when a published post is corrected |
| `lang` | `bg` \| `en` | no, default `bg` | rendered as `<article lang>`; `en` posts go under `research/` |
| `tags` | string[] | no | lowercase kebab-case (`/^[a-z0-9]+(-[a-z0-9]+)*$/`), English |
| `heroImage` | string | no | path relative to `public/`; falls back to `og-default.png` |
| `draft` | boolean | no, default `false` | drafts render in `npm run dev` only |

### Tags = categories

- Every tag used by a published post gets `/blog/tag/<tag>/`; `/blog/tag/` lists
  them all with counts, most used first. Nothing is configured anywhere else.
- **Synonym control** is procedural plus mechanical: the drafting agent runs
  `npm run tags` and reuses existing tags (the `/new-post` skill requires it), and
  the schema rejects anything that is not lowercase kebab-case, so `LLMs`/`llm`
  cannot coexist.
- Merging two tags later = edit the posts' frontmatter; the old tag page
  disappears. If the old tag page had traffic, add an nginx 301.

## 6. SEO and agent-readability

| Feature | Where |
|---|---|
| `<title>`, meta description, canonical (absolute, with `/blog/`) | `BaseLayout.astro` |
| Open Graph + Twitter card, `article:published_time`, `article:tag` | `BaseLayout.astro` |
| JSON-LD `Blog` (index) and `BlogPosting` with `Person` + `Organization` | `lib/schema.ts` |
| Sitemap `/blog/sitemap-index.xml` | `@astrojs/sitemap`; announced in root `robots.txt` |
| RSS `/blog/rss.xml`, `<language>bg</language>` | `pages/rss.xml.ts` |
| `/blog/llms.txt` | `pages/llms.txt.ts` |
| `noindex` on drafts (dev) and the 404 page | `BaseLayout.astro` |

Public wording rules baked into `site.config.ts`: "SciScend", never "SciScend ЕООД"
(nothing is registered yet); the author description follows the approved wording
in the workspace's `company/iva-popova-bio-short.md` — never "д-р" or "PhD".

## 7. Design

- Brand colours from the logo: ink `#353535`, teal `#13b0a5`, blue `#0050a7`.
  Teal fails contrast as text on white (≈ 2.6:1), so links use the blue and teal
  is used for accents only: the heading rule, tag chips, blockquote and author-box
  borders, hover underlines.
- Dark theme via `prefers-color-scheme`, no toggle.
- Single 42 rem column; the header collapses to a smaller logo and tighter nav
  under 30 rem. Tables scroll horizontally instead of breaking the layout.
- Header: logo mark (cropped from `brand/logo/logo_square_transparent.png`) +
  "SciScend / Блог"; nav: Статии, Категории, RSS. Footer links to the root domain.

## 8. Serving

On the VPS:

```
/var/www/sciscend.com/
├── html/   ← the placeholder   (deploy/placeholder/, npm run deploy:placeholder)
└── blog/   ← the blog           (dist/,               npm run deploy)
```

`html/` and `blog/` are siblings, so each `rsync --delete` mirrors only its own
tree. nginx (`deploy/nginx-sciscend.conf`):

- `location = /blog` → 301 to `/blog/`.
- `location ^~ /blog/` with `root /var/www/sciscend.com`,
  `try_files $uri $uri/index.html =404`, `error_page 404 /blog/404.html`,
  `charset utf-8`, HTML `must-revalidate`, security headers.
- **`^~` is required**: without it the server-level image regex wins for
  `/blog/*.png` and looks under `html/`. Asset caching for the blog is therefore
  nested inside the block: `_astro/` 1 year immutable, images 30 days; exact
  locations fix the MIME types of `rss.xml`, the sitemaps and `llms.txt`.
- The root `robots.txt` (in `deploy/placeholder/`) allows everything and points to
  the blog sitemap.

Cloudflare proxies the domain. Two Cloudflare settings affect the blog and are
dashboard decisions (see §11): Email Address Obfuscation rewrites `mailto:` links,
and managed `robots.txt` (not active as of 2026-09-22).

## 9. Deploy

```bash
npm run deploy              # build locally → rsync --delete dist/ → bulinfo:/var/www/sciscend.com/blog/
npm run deploy:placeholder  # rsync --delete deploy/placeholder/ → bulinfo:/var/www/sciscend.com/html/
```

Both scripts read `deploy/deploy.env` (gitignored; the `bulinfo` SSH alias holds
host, user and key) and refuse to run if the target path does not end in `/blog`
or `/html` respectively. nginx changes: edit `deploy/nginx-sciscend.conf`, then
the procedure in `deploy/README.md` (backup → `nginx -t` → reload).

## 10. Publishing workflow

`/new-post` (`.claude/skills/new-post/SKILL.md`):

1. **Draft** from Iva's topic and notes → `src/content/blog/<slug>.md`,
   `draft: true`, tags reused via `npm run tags`.
2. **Check**: `npm run build`; the workspace's `bin/redact-private-data.py
   --dry-run` plus the `check-private-data` reading pass; public wording rules.
3. **Iva edits**, previewing with `npm run dev`.
4. **Publish** (`/new-post publish <slug>`): `draft: false` → `npm run deploy` →
   verify 200 + RSS → commit and push.
5. **LinkedIn** (`/new-post linkedin <slug>`): native post, link in the first
   comment, saved to `social/linkedin/<slug>.md`.

## 11. Verification (2026-09-22)

- Build: 3 pages with the draft hidden; with test posts published: post page,
  `research/` path, two tag pages, RSS, sitemap and `llms.txt` all generated with
  absolute `/blog/` URLs. A tag `LLMs` failed the build as intended.
- Visual: headless Chrome screenshots at 1200 px (light) and 390 px (dark).
- Live, both at the origin (`curl --resolve`) and through Cloudflare: `/` 200,
  `/robots.txt` 200, `/blog` 301 → `/blog/`, `/blog/`, `/blog/tag/` 200,
  `rss.xml` `application/rss+xml`, sitemaps `application/xml`, `llms.txt`
  `text/plain; charset=utf-8`, images 200, unknown path and the draft 404 with
  the blog's 404 page, `_astro/` served `immutable`.

## 12. Open items

- **Cloudflare Email Address Obfuscation** is on: `lab@sciscend.com` in the footer
  is rewritten to `/cdn-cgi/l/email-protection`. Decide in the dashboard.
- **Google Search Console**: add the `sciscend.com` property and submit
  `https://sciscend.com/blog/sitemap-index.xml` (needs Iva's Google account).
- **`hreflang`**: add when the first post exists in both languages (e.g. a
  `translationOf` field linking the two).
- **Author page / social links**: `sameAs` in the `Person` JSON-LD once LinkedIn
  and GitHub profile URLs are to be public.
- **Migration into the future website**: keep the `/blog/<slug>/` URLs; move the
  content collection as-is.
