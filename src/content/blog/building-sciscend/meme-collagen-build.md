---
title: "Four Prompts, 85 Tests: What an Agent Finishes When You Say 'Make Sure It Works'"
description: 'Three sentences built the app. Eight more words, ''make sure it works'', made an agent write its own tests and catch bugs in code it had just written.'
pubDate: 2026-07-28
lang: en
tags: [building-in-public, ai-agents, claude-code, testing, vanilla-js]
transcript: ai/sessions/published/2026-07-28-meme-collagen-build.md
draft: true
---

> *Series: Building SciScend with AI — a solo founder building an entire company
> with AI as the workforce, documented as it happens.*

I gave an agent three sentences and got back an application I would have quoted
two weeks for. That part is no longer surprising to anyone who has used these
tools. The part worth writing down is what happened after I typed eight more
words: *"grate - do all of them. And make sure it works."*

Those eight words were the whole engineering process. The agent built its own
headless browser test suite, ran it, found four real bugs in code it had written
minutes earlier, fixed them, took screenshots of the result, looked at the
screenshots, and found three more problems the tests could not see. I watched
none of it. I was away from the machine for most of the evening.

## What I needed

Nothing important, deliberately. I wanted a meme and collage editor — pick some
pictures, arrange them, put captions on top, export a PNG. A throwaway tool.

The real question was different: **how far does unattended agent work actually
go before it needs me?** I teach this stuff, and I sell automation built on it,
so I cannot afford to have a marketing answer to that question. I need a
measured one.

The constraints came from being a one-person company. Whatever gets built, I
maintain alone. So: no dependencies, no build step, no server, no framework I
would need to keep upgrading. It had to open from a `file://` URL and work.

That last constraint turned out to matter more than it looks. It quietly killed
a category of decisions — ES modules are CORS-blocked on `file://`, so the agent
used classic `<script>` tags and never had to reason about bundling again. A
sharp constraint is worth more to an agent than a long specification.

## How the AI setup worked

Claude Code, Claude Opus 5, auto mode — meaning the agent runs its own tool calls
without asking me to approve each one. Four prompts across one evening. Here is
the first, exactly as I typed it:

```
build this project: meme-collage-generator. Simple interface.
Basic functionality:
1. user can upload image.
2. user can add text boxes on image.
3. user can change text size and color.

If i miss something - tell me.
```

That last line is the highest-leverage thing in this post. The agent built the
three features, then came back with seven things I had not asked for and an
argument for each: undo/redo ("the most likely thing to frustrate you"),
persistence, cropping, text wrapping, touch gestures, custom fonts, templates.
It also pointed out that Impact — the classic meme typeface — is not installed on
most Linux machines, so the look I was implicitly asking for would silently fail.

I did not evaluate the list carefully. I typed eight words:

```
grate - do all of them. And make sure it works.
```

Typo included. That authorized a rewrite: the single `app.js` became five focused
files, roughly 2,400 lines. Two later prompts asked for documentation following
GitHub conventions, and settled the name — the agent proposed *Collagen* for the
collage/generator pun, I countered with *MemeCollagen*, it agreed and explained
why the longer name was actually better (plain "collagen" is a protein, and
search results would be muddied).

Measured from the session transcript:

| | |
|---|---|
| Human prompts | **4**, about 456 characters total |
| Active time | **~1 h 13 min** across an eight-hour evening, mostly idle |
| Agent turns / tool calls | 231 / 128 |
| Application code | 2,436 lines |
| Tests | 85 browser checks, passing over `http://` and `file://` |

## What happened — including what failed

Plenty failed. That is the interesting half.

**The agent found its own bugs, and the good ones were subtle.** Four were real:

- `setPointerCapture` throws in some conditions, and because it was the first
  statement in the `pointerdown` handler, the exception meant *no gesture was
  ever created*. Every drag silently dead.
- Re-applying a collage layout progressively zoomed each crop further in — the
  crop was only ever shrunk to fit a new frame aspect, never re-expanded. Grid →
  columns → grid took an 800×400 image's crop from 640×400 down to 124×77. You
  would only notice this after several layout changes, which is exactly the kind
  of bug that survives manual testing.
- In crop mode the "ghost" of the part being cut away was drawn *behind*
  neighbouring images, so in a collage you could not see what you were panning.
- Template captions snapped to the canvas edge as one line, then slid off-screen
  the moment you typed a longer caption.

That last one needed two attempts. The first fix measured the text block properly
and looked correct in isolation; the screenshot still showed the caption bleeding
off the top, because the real workflow is *snap first, then type more*. The
second fix introduced edge pinning — text placed by a template stays pinned and
grows inward, and dragging it releases the pin.

**Several failures were the test's fault, not the app's**, and the agent said so
rather than "fixing" working code. A colour check sampled one pixel that landed
in the gap between two glyphs. An alignment test counted white pixels that
belonged to the test images. A pinch test asserted against a different layer than
the one the first finger actually landed on. Each was diagnosed as a test
artifact and the test was corrected. This distinction — *is the code wrong, or is
the test wrong?* — is the thing I would have expected an agent to get wrong most
often, and it did not.

**Screenshots caught what tests could not.** Pixel assertions cannot tell you a
speech-bubble outline is too thin to see at `lineWidth = size * 0.06`. The agent
rendered the real UI headlessly, read the PNGs back, and found three visual
problems that way.

**Its own tooling broke twice.** The test runner reported "No results" because
`chrome | python3 - <<'PY'` let the heredoc shadow the piped stdin — the parser
was reading its own source instead of the DOM. And earlier, the harness did
`rm -rf` on a build directory where it had written its only copy of the test
file, deleting it. Both were diagnosed and fixed without me.

**The session ran out of context and needed compacting** halfway through. Anyone
who has run long agent sessions knows this; the recovery was clean, but it is not
a frictionless process and I am not going to pretend otherwise.

**It refused to invent facts about me.** The Code of Conduct needs an enforcement
address, and rather than dropping my personal email into a file heading for a
public repo, it left `CONTACT_EMAIL_HERE` and told me to fill it in. Same with the
GitHub username in badge URLs. That is the correct behaviour, and it is the kind
of restraint I would not have thought to ask for.

The one genuinely wasted turn was mine: I typed `/рц` — a slash command with the
keyboard still in Cyrillic. It correctly guessed I meant `/run`.

## The pattern to steal

Strip out the memes and this is what transfers:

- **Add "if I miss something, tell me" to the end of your first prompt.** It cost
  me nine words and produced a seven-item gap analysis with reasoning. Asking for
  a critique of your own specification is the cheapest upgrade available.
- **"Make sure it works" is load-bearing.** It is what converts code generation
  into a verification loop. The agent built a harness that drives the *real*
  `index.html` — the runner rebuilds a throwaway copy of the actual app with the
  tests appended, so the tests cannot drift from what ships.
- **Give it one sharp constraint that kills a category of decisions.** "Must open
  from `file://`" did more work than any amount of architecture description.
- **Let it look at its own output.** Not just exit codes — screenshots, rendered
  pages, actual pixels. A meaningful class of bugs is only visible that way.
- **Ask it to distinguish test failures from code failures explicitly.** Some of
  those 85 checks were wrong, and being told which is more valuable than a green
  suite.
- **Then verify the claim yourself.** I ran the suite on a clean checkout before
  publishing anything: 85/85 in both modes. "The agent wrote tests" is a weak
  claim; "the tests pass on a machine that isn't the one that wrote them" is not.

And the limit worth stating plainly: **these are the agent's own tests.** They
prove the app does what it was built to do and does not regress. They cannot
prove the specification was right. Nobody has yet checked whether this tool is
pleasant to use — that requires a human, and it is still the part that does not
automate.

The code is public, the test suite runs in one command, and the whole session
transcript is linked below. If you think four prompts is an exaggeration, the
receipts are all there.

- **Try it:** <https://sciscend.github.io/meme-collagen/>
- **Source:** <https://github.com/SciScend/meme-collagen>

Next: publishing it properly — why company code goes to an organization account
from the first commit, and how one machine juggles several git identities
without ever committing under the wrong one.

<!-- DRAFT NOTES (remove before publishing):
- The paragraph before "Try it" still says the transcript is linked below; the
  link moved to the `transcript:` frontmatter, so reword or drop that sentence.
- CODE_OF_CONDUCT.md in the repo still had CONTACT_EMAIL_HERE at publish time; set
  to lab@sciscend.com. Change if abuse reports should go elsewhere.
- No screenshots embedded in this post yet. docs/screenshot.png, docs/crop.png and
  docs/bubble.png in the meme-collagen repo are the obvious candidates.
- Claim check before publishing: "I would have quoted two weeks for it" — keep or
  soften? It is an honest estimate but unverifiable.
-->
