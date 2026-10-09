---
title: "How I Named My Company with a Two-Agent AI Pipeline"
description: 'How I named my company with two AI agents: one generates names, the other checks registers, domains, trademarks and meanings across languages.'
pubDate: 2026-07-18
lang: en
tags: [building-in-public, ai-agents, claude-code, naming, solo-founder]
draft: true
---

> *Series: Building SciScend with AI — a solo founder building an entire company
> with AI as the workforce, documented as it happens.*

I'm building my company alone — no employees, no agency, no co-founder. My
workforce is AI. This series documents how that actually works, task by task,
with the real prompts and real outputs. First up: the company name.

## The task nobody enjoys

Naming a company means one creative afternoon and then a swamp of mechanical
checking: is it taken in the companies register? Is the .com free, and at what
price across four registrars? Does someone own it on Instagram? Does it mean
something embarrassing in German? Is there a similar EU trademark in your
category? Each check is trivial; together they kill weeks.

That split — *cheap mechanical checks* versus *subtle judgment* — is exactly
where AI agents shine. So I built a two-agent pipeline.

## Agent 1: the Brand Strategist

The first agent got a persona (verbal identity expert), my company context, and a
strict job: generate 10–15 candidates, then screen them against **ordered
constraints, cheapest check first**:

1. Bulgarian Companies Register — found? Discard immediately.
2. Negative associations on the web and social platforms — discard.
3. Domain availability (.com / .ai / .bg) — none free? Discard.
4. Only *then* score survivors on trust, catchiness, market fit, scalability, SEO.

The ordering matters: most names die at a lookup that costs seconds, so the
expensive scoring effort is spent only on real contenders.

## Agent 2: the Name Evaluator

The second agent read Agent 1's results file and did the work that needs
judgment: pronunciation friction across Bulgarian, English, and major EU
languages (with IPA transcriptions!), spelling-ambiguity risk, cross-language
connotation checks, EUIPO/USPTO trademark proximity, and a brand narrative for
each finalist.

One line in its prompt did a lot of heavy lifting: **"Do not repeat that work."**
Without it, a second agent happily re-verifies everything the first one did and
burns its budget on redundancy. The agents talked through a single structured
Markdown file at a fixed path — no shared memory, fully auditable, restartable.

## What the pipeline gave me — and what it didn't

The output was a ranked shortlist with explicit trade-offs. Interestingly, I
didn't pick the top-ranked name. The phonetically "safest" candidates felt
generic; **SciScend** ("science" + "ascend") carried the story I wanted, with a
known, accepted risk: people will sometimes type "SciSend". The pipeline's job
wasn't to decide — it was to make the trade-offs sharp enough that *I* could
decide in minutes instead of weeks.

## The pattern to steal

**Facts first, judgment second, human last.**

- One agent does cheap verifiable screening, ordered by cost of checking.
- A second agent reasons deeply — but only about survivors, and told explicitly
  not to redo the screening.
- A structured handoff file is the entire interface between them.
- The human makes the final call on a clean decision surface.

I've since turned the pipeline into a reusable slash-command in my repo, and the
same pattern — screen, evaluate, choose — is next going to pick my course
platform.

*Next in the series: registering a Bulgarian ЕООД with an AI-drafted legal
package — no lawyer, no intermediary, 55 лв. in state fees.*

<!-- DRAFT NOTES (remove before publishing):
Source prompts in the SciScend workspace: ai/prompts/2026-03-15-company-naming-pipeline/
- Decide blog language strategy (EN vs EN+BG) before first publish.
- Add 1-2 screenshots: scoring table from naming-brainstorm, evaluation table HTML.
- Verify: OK to show real candidate names that were rejected? (they're public in repo anyway if repo goes public — decide repo visibility first)
-->
