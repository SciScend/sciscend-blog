# SciScend blog

Source of **https://sciscend.com/blog/** — practical AI, Python and machine learning
in Bulgarian: tests of new models, beginner guides, AI for small business.

Static [Astro](https://astro.build/) site, served by nginx under `/blog/`. The
homepage `/` is a separate coming-soon placeholder, versioned in
`deploy/placeholder/`.

```bash
npm install
npm run dev          # http://localhost:4321/blog/ — drafts visible here only
npm run tags         # tags in use, to reuse when tagging a new post
npm run build        # validates every post's frontmatter
npm run deploy       # build + rsync to the VPS (see deploy/README.md)
```

A post is a Markdown file in `src/content/blog/`; its path is its URL. New posts
are drafted and published with the `/new-post` Claude Code skill.

- [docs/tech-spec.md](docs/tech-spec.md) — how it is built, served and published
- [deploy/README.md](deploy/README.md) — deploy and nginx runbook

---

Built with Claude Opus 5.5 via Claude Code. Published by [SciScend](https://sciscend.com/).
