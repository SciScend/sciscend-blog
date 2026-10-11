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
are drafted and published with the `/blog-post` Claude Code skill.

## Publishing a draft

`/blog-post publish <path>` (e.g. `novini/rea-reverse-engineer-anything`) runs:

1. `draft: false` in the frontmatter; `pubDate` set to today if the draft is older.
2. Checks: `npm run build` (schema, and the News format for `novini/`), then the
   SciScend workspace's `bin/redact-private-data.py <file> --dry-run` and the
   `check-private-data` reading pass.
3. `npm run deploy`.
4. Verify: `https://sciscend.com/blog/<path>/` returns 200 and the post is in
   `rss.xml`.
5. Commit `Publish: <title>` and push.

The LinkedIn announcement follows with `/linkedin-post from-blog <path>` in the
SciScend workspace.

- [docs/tech-spec.md](docs/tech-spec.md) — how it is built, served and published
- [deploy/README.md](deploy/README.md) — deploy and nginx runbook

## License

Code: [MIT](LICENSE). Articles, images and the SciScend brand assets: all rights
reserved — see [LICENSE-CONTENT.md](LICENSE-CONTENT.md).

---

Built with Claude Opus 5.5 via Claude Code. Published by [SciScend](https://sciscend.com/).
