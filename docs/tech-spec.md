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
| Posts in Bulgarian or English at `/blog/<slug>/`; R&D texts under `/blog/research/` | `hreflang` pairs (added with the first translated post) |
| The coming-soon placeholder at `/` and the Cloudflare Worker configs | |
| The "Building SciScend with AI" series under `/blog/building-sciscend/` (drafts; moved from the workspace 2026-10-09) | |
| The News section: short news items under `/blog/novini/`, listed at `/blog/novini/` and in the main list with a "новини" badge (added 2026-10-11) | |

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
7. **Static only.** Cloudflare Workers serve the files (static assets, no Worker
   code); builds happen on the laptop.

## 3. Stack

| Part | Choice |
|---|---|
| Generator | Astro 7, static output, `@astrojs/mdx` |
| Feeds / SEO | `@astrojs/rss`, `@astrojs/sitemap`, hand-written JSON-LD and `llms.txt` |
| Styling | one hand-written stylesheet, `src/styles/global.css` — no framework |
| Fonts | system font stack (Cyrillic-complete, zero requests) |
| Code highlighting | Shiki, dual theme (`github-light` / `github-dark`) |
| Hosting | Cloudflare Workers static assets (`sciscend-blog`, `sciscend-home`), since 2026-11-03; before that the Bullinfo VPS with nginx |
| Repo | `github.com/SciScend/sciscend-blog` (private), local `/data/projects/sciscend-blog` |

Key `astro.config.mjs` settings: `site: 'https://sciscend.com'`, `base: '/blog'`,
`trailingSlash: 'always'`, `build.format: 'directory'`. The build output in `dist/`
is *unprefixed* (`dist/index.html`, `dist/tag/…`); the prefix comes from where it
is deployed (`deploy/deploy.sh` stages it as `dist-cf/blog/`).

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
│       ├── [...slug].astro     /blog/<slug>/  and  /blog/<folder>/<slug>/
│       ├── novini/index.astro  /blog/novini/         the news items only
│       ├── tag/index.astro     /blog/tag/            all tags with counts
│       ├── tag/[tag].astro     /blog/tag/<tag>/
│       ├── rss.xml.ts          /blog/rss.xml
│       ├── llms.txt.ts         /blog/llms.txt
│       └── 404.astro           /blog/404.html
├── public/                     logo, favicons, default share image, post images, _headers (Cloudflare)
├── scripts/tags.mjs            `npm run tags` — tags in use with counts
├── scripts/check-news.mjs      `npm run check:news` — news format check, run before every build
├── scripts/make_diagrams.py    SVG diagrams for the System One / Jev series (python3; see its docstring)
├── deploy/
│   ├── deploy.sh               `npm run deploy` (Cloudflare Worker sciscend-blog)
│   ├── deploy-placeholder.sh   `npm run deploy:placeholder` (Worker sciscend-home)
│   ├── cloudflare-env.sh       loads the Cloudflare credentials for the two above
│   ├── placeholder/            the coming-soon page + root robots.txt, _headers, _redirects
│   └── README.md               runbook
├── wrangler.jsonc              Cloudflare Worker sciscend-blog
├── wrangler.home.jsonc         Cloudflare Worker sciscend-home (the placeholder)
├── .claude/skills/blog-post/   /blog-post — draft, check, publish
└── docs/tech-spec.md           this file
```

## 5. Content model

One Markdown/MDX file per post in `src/content/blog/`. The path is the URL:

| File | URL |
|---|---|
| `src/content/blog/jev-na-balgarski.md` | `/blog/jev-na-balgarski/` |
| `src/content/blog/research/foo.md` | `/blog/research/foo/` |
| `src/content/blog/building-sciscend/foo.md` | `/blog/building-sciscend/foo/` |
| `src/content/blog/novini/foo.md` | `/blog/novini/foo/` (a news item) |

Slugs are Latin, kebab-case, transliterated, without a date, 2-5 words and at
most 40 characters, specific about the topic; the full rule is in the
`/blog-post` skill (step 1.3). A slug is free to change until the post is
published; after that it is a permanent URL.

Frontmatter (validated by `src/content.config.ts`; a violation fails the build):

| Field | Type | Required | Notes |
|---|---|---|---|
| `title` | string | yes | ≤ 70 characters recommended |
| `description` | string | yes | 120–160 characters; meta description, OG, RSS, listing |
| `pubDate` | date | yes | |
| `updatedDate` | date | no | set when a published post is corrected |
| `lang` | `bg` \| `en` | no, default `bg` | rendered as `<article lang>`; does not set the path - `research/` is for R&D texts, `building-sciscend/` for the series |
| `tags` | string[] | no | lowercase kebab-case (`/^[a-z0-9]+(-[a-z0-9]+)*$/`), English |
| `heroImage` | string | no | path relative to `public/`; falls back to `og-default.png` |
| `transcript` | string | no | workspace path of the redacted session transcript the post came from (series posts); never rendered |
| `linkedin_url` | URL | no | the LinkedIn post announcing it; the workspace LinkedIn file links back with `blog_url:`; never rendered |
| `draft` | boolean | no, default `false` | drafts render in `npm run dev` only |

### News items

A post in `src/content/blog/novini/` is a news item; there is no frontmatter field
for it (`isNews()` in `lib/posts.ts` checks the folder). News items appear in the
main list with a "новини" badge, and alone on `/blog/novini/` (menu: Новини).
Their format (100-300 words, no sections, source linked in the text, no hashtags
or LinkedIn leftovers, 2-4 tags, description 120-160 characters) is checked by
`scripts/check-news.mjs`, which `npm run build` runs first: a published item that
breaks it fails the build, a draft gets warnings. The rules are in the
`/blog-post` skill, "News format".

### Tags = categories

- Every tag used by a published post gets `/blog/tag/<tag>/`; `/blog/tag/` lists
  them all with counts, most used first. Nothing is configured anywhere else.
- **Synonym control** is procedural plus mechanical: the drafting agent runs
  `npm run tags` and reuses existing tags (the `/blog-post` skill requires it), and
  the schema rejects anything that is not lowercase kebab-case, so `LLMs`/`llm`
  cannot coexist.
- Merging two tags later = edit the posts' frontmatter; the old tag page
  disappears. If the old tag page had traffic, add a 301 in `public/_redirects`.

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

Three Cloudflare Workers with static assets only (no code) serve sciscend.com
since 2026-11-03 (workspace: decision 021):

| Route | Worker | From |
|---|---|---|
| `sciscend.com/blog/*` | `sciscend-blog` | this repo, `dist/` staged as `dist-cf/blog/` |
| `sciscend.com/ivapopova/*` | `sciscend-portfolio` | the workspace, `bin/build-portfolio.py` |
| `sciscend.com/*` | `sciscend-home` | this repo, `deploy/placeholder/` |

The most specific route wins. Each Worker is deployed on its own, so a blog
deploy never touches the placeholder and the other way round.

- `html_handling: auto-trailing-slash`: `/blog/x` answers 307 to `/blog/x/`.
- `not_found_handling: 404-page`: `/blog/404.html` with status 404.
- `public/_headers`: security headers, HTML `charset=utf-8` and
  `must-revalidate`, `_astro/` 1 year immutable, images and fonts 30 days, the
  MIME types and 1-hour cache of `rss.xml` and `llms.txt`.
- `/blog` -> `/blog/` (301) is in `deploy/placeholder/_redirects`: without the
  slash the path is outside the blog route.
- The root `robots.txt` (in `deploy/placeholder/`) allows everything and points to
  the blog sitemap.

Zone settings that affect the blog (see §11 and the workspace's
`operations/hosting-and-deployment.md`): Email Address Obfuscation rewrites
`mailto:` links; the AI crawler policies must stay on Allow so that Cloudflare
does not prepend its managed block to `robots.txt` (it did until 2026-11-03).

## 9. Deploy

```bash
npm run deploy              # build -> dist-cf/blog/ -> wrangler deploy (Worker sciscend-blog)
npm run deploy:placeholder  # wrangler deploy deploy/placeholder/ (Worker sciscend-home)
```

Credentials come from `deploy/cloudflare-env.sh` (default: the workspace's
`.private/cloudflare.env`). Details, the checks, redirects and the `base_path`
workaround: `deploy/README.md`.

## 10. Publishing workflow

`/blog-post` (`.claude/skills/blog-post/SKILL.md`):

1. **Draft** from Iva's topic and notes, after asking for the language (`bg` or
   `en`) and the placement (root, `research/`, `novini/` or `building-sciscend/`) ->
   `src/content/blog/<path>.md`, `draft: true`, tags reused via `npm run tags`.
   Series posts are drafted instead by `/blogworthy` in the SciScend workspace,
   from a real session, into `building-sciscend/`; from step 2 on they follow the
   same steps.
2. **Check**: `npm run build`; the workspace's `bin/redact-private-data.py
   --dry-run` plus the `check-private-data` reading pass; public wording rules.
3. **Iva edits**, previewing with `npm run dev`.
4. **Publish** (`/blog-post publish <path>`): `draft: false` -> `npm run deploy` ->
   verify 200 + RSS -> commit and push.
5. **LinkedIn**: `/linkedin-post from-blog <path>` in the SciScend workspace
   writes the announcement into `marketing/social/linkedin/`, after asking for its
   language and channel. Once it is live, the two link each other: `linkedin_url:`
   in the blog post, `blog_url:` (and `url:`) in the LinkedIn file.

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
