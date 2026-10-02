---
name: blog-post
description: Draft a new article for the SciScend blog (sciscend.com/blog) from Iva's topic and notes — Bulgarian by default, tagged with existing tags, checked for private data, saved as a draft. Also publishes a finished draft. Use when Iva types /blog-post, or asks to write, draft or publish a blog article.
---

# /blog-post — from topic to published article

The blog is Iva's voice: her tests, her position, her explanations. Your job is the
mechanical and editorial work around that voice — drafting from her notes,
formatting, tags, checks, publishing. Never invent a test result, a benchmark
number, a quote or an opinion she did not give you. If the notes are too thin to
carry an article, say what is missing and ask; do not pad.

    /blog-post Тествах JeV на български текстове — бележки: …
    /blog-post publish jev-na-balgarski          # publish an existing draft

The LinkedIn post that announces a published article is not written here: it is
`/linkedin-post from-blog <slug>` in the SciScend workspace, where all LinkedIn
posts live.

## 1. Draft

1. **Material.** Take the topic and notes from the prompt. Read any files or links
   Iva points to. For facts about a new model or tool, check the primary source
   (vendor page, paper, model card) and cite it in the text; say so when you could
   not verify something.
2. **Language.** Bulgarian unless Iva says otherwise (`lang: bg`). Technical terms
   stay in English — pipeline, prompt, fine-tuning, benchmark, commit — never
   literal translations. English posts (`lang: en`) go under `research/`.
3. **Slug and file.** `src/content/blog/<slug>.md` (or `.mdx` if the post needs
   components). The slug is short, Latin, kebab-case, transliterated from the
   Bulgarian title, no date: `jev-na-balgarski`, not `2026-09-22-jev`. The slug is
   the permanent URL, so choose it once.
4. **Tags.** Run `npm run tags` and **reuse** existing tags. Add a new tag only
   when the topic is genuinely new, and never a near-duplicate (`llm` exists →
   not `llms`, not `language-models`). Lowercase kebab-case, English, 2–5 per
   post. The build rejects anything else.
5. **Frontmatter:**

   ```yaml
   ---
   title: '…'                 # ≤ 70 characters, says what the reader gets
   description: '…'           # 120–160 characters; meta description + share text
   pubDate: YYYY-MM-DD        # today
   lang: bg
   tags: [ … ]
   draft: true
   ---
   ```

6. **Shape.** Start with the point, not with background. Short paragraphs, `##`
   sections, code in fenced blocks with a language, tables for comparisons.
   Beginner posts explain every step; test posts show the setup, the inputs and
   the actual outputs so a reader can repeat them. End with Iva's conclusion in
   her words from the notes — not a generic summary.
7. **Images** go to `public/images/<slug>/` and are referenced as
   `/blog/images/<slug>/<file>`. Set `heroImage: images/<slug>/<file>` if one
   should be the share image.

## 2. Check

1. `npm run build` must pass (the schema validates the frontmatter).
2. **Private data.** The post is about to become public:
   - `/data/projects/SciScend/bin/redact-private-data.py <file> --dry-run`
   - then do the reading pass described in
     `/data/projects/SciScend/.claude/skills/check-private-data/SKILL.md`
     (named third parties, clients, figures, infrastructure details such as
     server IPs or paths, unreleased plans). Report findings; change only what
     Iva approves.
3. **Public wording rules.** "SciScend", never "SciScend ЕООД" (nothing is
   registered yet). Never "д-р", "PhD" or "доктор" for Iva — the approved author
   wording is in `src/site.config.ts`.
4. Tell Iva the draft is ready and how to see it: `npm run dev` →
   `http://localhost:4321/blog/<slug>/` (drafts are visible only in dev).

Stop here. Iva edits the text herself.

## 3. Publish (`/blog-post publish <slug>`)

1. Set `draft: false`. If the post was drafted days ago, set `pubDate` to today
   (ask if unsure). If it was already published and is being corrected, leave
   `pubDate` and set `updatedDate` to today instead.
2. `npm run build`, then `npm run deploy`.
3. Verify: `curl -s -o /dev/null -w "%{http_code}\n" https://sciscend.com/blog/<slug>/`
   returns 200, and the post appears in `https://sciscend.com/blog/rss.xml`.
4. Commit (`Publish: <title>`) and push.
5. Tell Iva the LinkedIn announcement is `/linkedin-post from-blog <slug>` in the
   SciScend workspace.
