---
title: "The AI Workflow I Designed and Never Followed"
description: 'I asked an AI to audit the session-archiving workflow I had designed. It found I had never followed it once, and that I never could have.'
pubDate: 2026-07-25
lang: en
tags: [building-in-public, ai-agents, claude-code, tooling, solo-founder]
draft: true
---

> *Series: Building SciScend with AI — a solo founder building an entire company
> with AI as the workforce, documented as it happens.*

I'm building my company alone, with AI as the workforce, and I want the building
itself to be public. That means keeping the sessions: what I asked, what came
back, what went wrong. Months ago I set up a pipeline for exactly this — a
journal of prompts, a folder for outputs, case studies distilled from both, blog
posts distilled from the case studies. It was written down in the repo rules. It
looked sensible.

This week I asked for an audit of it. The answer was that I had never once
followed it, and could not have.

## What the audit found

The rule said every journal entry must record the date, the model, and a link to
its output. Of the eight entries in the journal, **zero** had any of the three.
They were bare prompt text. The `output/` folder the rules kept referring to was
empty. One entry still carried a four-bullet description of my company that
predated a whole business pillar, because the company context had been pasted by
hand into each prompt and then drifted.

The interesting part wasn't the sloppiness. It was *why* a rule I wrote for
myself was unfollowable.

**It assumed the wrong unit of work.** A journal entry holds one prompt and one
answer. That's the shape of a ChatGPT exchange. A Claude Code session is forty
turns with tool calls, corrections and dead ends, and the dead ends are the part
worth publishing. There was nowhere to put them.

**It asked me to re-type what the machine already had.** Every session is already
stored as JSONL under `~/.claude/projects/`. I had thirty-six of them, 142 MB,
completely unused by a pipeline whose main activity was copying their contents
back into the repo by hand.

**It deferred the write-up to a moment when it becomes unaffordable.** Writing up
a session from its transcript means reading the transcript. One of mine is 3 MB —
roughly 750,000 tokens to read back. Writing the same summary at the end of the
session, while it's still in the model's context, costs a few hundred. That is
three orders of magnitude, and it's the whole ballgame.

## What replaced it

Three artefacts, three commands. Nothing polished unless I ask for it.

**Prompts in.** I like writing prompts in my editor, not in a terminal box, and I
often want the same prompt sent to Gemini or GPT for comparison. So: I write only
the prompt text. A script generates the English slug (a headless `claude -p
--model haiku` call, using my existing subscription, no API key), adds the date
and the frontmatter, expands the company context *by reference to the files that
own it* rather than by copying, and puts the whole thing on the clipboard. Same
text everywhere, so a cross-model comparison is actually fair.

**Transcripts out.** A second script renders a session's JSONL as prose: my
questions, the model's answers, tool calls compressed to one line each. Thinking
blocks, tool output and harness bookkeeping dropped by default. The result is
something I can read on a train.

**Posts on demand.** A `/blogworthy` skill exports the session, redacts it, and
drafts a post. It runs when I say so and not otherwise.

One rule is written into the skill itself: *when writing up the current session,
work from context, not from the exported transcript.* The export exists so the
raw material survives in git, not so the model can re-read what it just lived
through.

Raw transcripts stay gitignored. A transcript contains everything that crossed
the screen, and this repo may go public; only vetted, redacted copies are tracked.

## What broke

Everything above is design. Here's what actually happened when it met real data.

**The dates were in UTC.** I work at night. A session that started at 02:00 local
got filed under the previous day. Invisible until you look at a filename and know
it's wrong.

**I read the wrong field.** The harness already names every session, and I wanted
to reuse that name instead of paying for a new one. I looked for `title`; the
field is `aiTitle`. So it silently fell through to the opening prompt, truncated
mid-word. Haiku received a chopped-off Bulgarian sentence, replied
conversationally to it, and that reply became a filename:
`your-message-appears-to-be-incomplete.md`.

**One session, two files.** Listing my sessions showed two entries with the same
start second and the same first prompt: one with 33 lines, one with 358. Comparing
them, 22 of 23 UUIDs were shared — the big file *contained* the small one. The
version stamps explained it: 2.1.219 in the first, 2.1.219 and 2.1.220 in the
second. Claude Code had updated mid-session; the restart minted a new session id,
replayed the history into a new file, and left the original frozen at the six
minute mark. My sort key was start time, and the two started in the same second,
so the tie broke on filesystem order. `--last` could have exported the stub
instead of the fifteen-hour session, at random.

Then I ran `/blogworthy` on this very session, and it found two more. The
redaction pattern for `.private/` paths was greedy: it matched the word in
ordinary prose, swallowed the closing backtick, and mangled three sentences to
protect nothing. And the slug was generated twice — once per export — so the raw
and published copies of the same session got two different names.

Five defects. Not one of them was visible in review; every one surfaced on real
transcripts within minutes of running the thing.

## The pattern to steal

- **Don't copy what the system already records.** Point at it. Your tool already
  keeps transcripts, your VCS already keeps diffs, your source files already own
  the facts. Every hand-maintained duplicate is a thing that drifts.
- **Capture while the context is hot.** Summarising a session you just finished is
  nearly free; reconstructing it later can cost a thousand times more. Put the
  cheap step in the workflow and the expensive step will never be needed.
- **Make the polished stage opt-in.** My original pipeline demanded a case study
  per session before anything could be published. A process that produces
  documents nobody reads stops being used entirely — which is exactly what
  happened.
- **A rule that isn't followed isn't a discipline problem.** It's a design defect.
  Look at what the rule asks you to do by hand and ask what already does it.
- **Dogfood on real data on day one.** UTC offsets, a misspelled field name, a
  version upgrade mid-session: no amount of reading the code would have found
  these.

The full transcript of this session, including the parts where I pushed back, is
[in the repo](../../../ai/sessions/published/2026-07-25-review-session-archiving-process.md).

*Next in the series: registering a Bulgarian ЕООД with an AI-drafted legal
package — no lawyer, no intermediary, 55 лв. in state fees.*

<!-- DRAFT NOTES (remove before publishing):
Source session in the SciScend workspace: ai/sessions/published/2026-07-25-review-session-archiving-process.md
- Decide repo visibility before linking the transcript publicly.
- Possible screenshot: the session list showing the twin sessions before the fix.
-->
