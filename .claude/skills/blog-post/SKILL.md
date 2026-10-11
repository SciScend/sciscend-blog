---
name: blog-post
description: Draft a new article or news item for the SciScend blog (sciscend.com/blog) from Iva's topic and notes - asks for the language (Bulgarian or English) and the placement (blog root, research/ or the novini/ news section), tags it with existing tags, checks it for private data, saves it as a draft. Also publishes a finished draft. Use when Iva types /blog-post, or asks to write, draft or publish a blog article or a news item.
---

# /blog-post — from topic to published article

The blog is Iva's voice: her tests, her position, her explanations. Your job is the
mechanical and editorial work around that voice — drafting from her notes,
formatting, tags, checks, publishing. Never invent a test result, a benchmark
number, a quote or an opinion she did not give you. If the notes are too thin to
carry an article, say what is missing and ask; do not pad.

    /blog-post Тествах JeV на български текстове — бележки: …
    /blog-post en, root: How I use Claude Code - notes: ...   # no question needed
    /blog-post publish jev-na-balgarski          # publish an existing draft
    /blog-post news: <notes, or a LinkedIn post file>   # a news item in novini/

The LinkedIn post that announces a published article is not written here: it is
`/linkedin-post from-blog <path>` in the SciScend workspace, where all LinkedIn
posts live.

## 1. Draft

1. **Material.** Take the topic and notes from the prompt. Read any files or links
   Iva points to. For facts about a new model or tool, check the primary source
   (vendor page, paper, model card) and cite it in the text; say so when you could
   not verify something.
2. **Language and placement.** Unless the prompt already says both, ask Iva
   before drafting, in one question:
   - language: Bulgarian (`lang: bg`, the default) or English (`lang: en`);
   - placement: the blog root, `/blog/<slug>/` (the default, for every post that
     is not R&D, news or the series), `research/` for R&D texts, `novini/` for a
     news item (short, follows the News format below), or `building-sciscend/`
     for the "Building SciScend with AI" series (normally drafted by
     `/blogworthy` in the SciScend workspace).

   In Bulgarian text, technical terms stay in English - pipeline, prompt,
   fine-tuning, benchmark, commit - never literal translations.
3. **Slug and file.** `src/content/blog/<slug>.md`, or
   `src/content/blog/<folder>/<slug>.md` for the `research/`, `novini/` and
   `building-sciscend/` placements (`.mdx` if the post needs components). The
   file's path without the extension, `<slug>` or `<folder>/<slug>`, is the
   `<path>`: the URL after `/blog/`, and what `/blog-post publish` and
   `/linkedin-post from-blog` take. The slug rule:
   - Latin, kebab-case, no date; transliterated if the title is Bulgarian:
     `jev-na-balgarski`, not `2026-09-22-jev`;
   - 2-5 words, at most 40 characters;
   - specific: keep the words that say what the post is about, including the
     object: `two-agent-company-naming-pipeline`, not `two-agent-naming-pipeline`;
   - no filler words (a, the, how, i, my, with, of, to) and no repeat of the
     folder name (no `sciscend` inside `building-sciscend/`);
   - shorten only a slug that breaks these limits; do not reword one that fits.

   A slug can change freely until the post is published. After that it is a
   permanent URL, and changing it needs an nginx 301 in
   `deploy/nginx-sciscend.conf`.
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
   lang: bg                   # or en, from step 2
   tags: [ … ]
   draft: true
   ---
   ```

6. **Shape.** Start with the point, not with background. Short paragraphs, `##`
   sections, code in fenced blocks with a language, tables for comparisons.
   Beginner posts explain every step; test posts show the setup, the inputs and
   the actual outputs so a reader can repeat them. End with Iva's conclusion in
   her words from the notes — not a generic summary.
7. **News items** follow the News format below instead of the article shape.
8. **Images** go to `public/images/<slug>/` and are referenced as
   `/blog/images/<slug>/<file>`. Set `heroImage: images/<slug>/<file>` if one
   should be the share image.

## News format (`novini/`)

A news item is a short take on something new in AI: what happened, then what Iva
thinks of it. It can start anywhere: from scratch here, or from one of her
LinkedIn posts in `/data/projects/SciScend/marketing/social/linkedin/` (copy her
text as is), and a LinkedIn post can also follow it. Whichever comes first, the
blog version looks the same:

- 100-300 words of plain paragraphs, no `##` sections;
- first what happened, then Iva's take, in her words;
- the source is linked in the text (`[REA](https://github.com/...)`), not in a
  "first comment";
- no hashtags and no LinkedIn leftovers ("линкът е в първия коментар"); topics go
  into 2-4 `tags`;
- a dated wording ("Днес (11.10.2026)") is fine: a news item is dated;
- `heroImage` optional; reuse the LinkedIn image if there is one, copied to
  `public/images/<slug>/`.

`npm run check:news` (also run by every `npm run build`) checks these rules
mechanically, plus title, description, tags and slug. A published item that breaks
them fails the build; a draft only gets warnings. When a LinkedIn post and a news
item exist for the same news, set `blog_url:` in the LinkedIn file's front matter.

## 2. Check

1. `npm run build` must pass (the schema validates the frontmatter; for a news
   item, `check-news.mjs` validates the format).
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
   `http://localhost:4321/blog/<path>/` (drafts are visible only in dev).

Stop here. Iva edits the text herself.

## 3. Publish (`/blog-post publish <path>`)

1. Set `draft: false`. If the post was drafted days ago, set `pubDate` to today
   (ask if unsure). If it was already published and is being corrected, leave
   `pubDate` and set `updatedDate` to today instead.
2. `npm run build`, then `npm run deploy`.
3. Verify: `curl -s -o /dev/null -w "%{http_code}\n" https://sciscend.com/blog/<path>/`
   returns 200, and the post appears in `https://sciscend.com/blog/rss.xml`.
4. Commit (`Publish: <title>`) and push.
5. Tell Iva the LinkedIn announcement is `/linkedin-post from-blog <path>` in the
   SciScend workspace. Once a LinkedIn post for it is live, link the two both
   ways: `linkedin_url: <LinkedIn post URL>` in the blog post's frontmatter, and
   `blog_url: https://sciscend.com/blog/<path>/` (plus `url:`) in the LinkedIn
   file. Commit and push both repos.
