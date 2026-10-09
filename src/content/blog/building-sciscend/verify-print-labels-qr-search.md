---
title: "\"Are We Sure It Works?\" Questioning an Agent About a Feature It Built"
description: 'I asked an agent whether a feature it had built actually works. The honest answer was ''not sure'', and the QR scanner I was looking for did not exist.'
pubDate: 2026-09-17
lang: en
tags: [building-in-public, ai-agents, claude-code, verification, pwa, capacitor]
transcript: ai/sessions/published/2026-09-17-verify-print-labels-qr-search.md
draft: true
---

> *Series: Building SciScend with AI: a solo founder building an entire company
> with AI as the workforce, documented as it happens.*

StorageBoxOrganizer is a small app I use to keep track of what is in the boxes in
my storage room. An agent built most of it. One of its features is a "Print
labels" button: it prints a sheet of labels, each with a QR code, to stick on the
real boxes. I had merged that feature weeks ago. Then I was writing a case study
about the app and realized I could not say whether printing actually works. I
also didn't know where in the app you scan a box. I own a product with a feature
I had never used and did not understand.

So at 2:40 in the morning I asked. I also started Claude in the wrong folder.

## What I needed

Three plain answers, and no code changes:

1. Does "Print labels" work?
2. How do I test it without a printer? Would a PDF do?
3. Where is the "find a box by QR code" option, and how does it work?

The constraint is ordinary for a one-person company: no printer at hand, no QA
person, and a feature whose author was a model. What I needed was an honest read
of the feature, not a new one.

## How the AI setup worked

I use a `/session` command for tasks like this. It opens VSCode, I write the
prompt there, and closing the tab files the prompt under `ai/prompts/` along
with a link to the live session, so I can follow along from my phone. When the
work ends, the outcome is written back into the same file:

```yaml
session: https://claude.ai/code/session_...
status: done
result: "Answer in session: how to test Print labels via PDF, how the QR link
  works, two problems found (Android APK, no in-app scanner); no code changes"
```

The prompt itself, in Bulgarian in the original, was just the three questions
above. My global instructions say a question gets an answer, not edits, and the
agent followed that. It only read files, and the only commit was the prompt
record.

## What happened, including what failed

**Wrong starting folder.** I launched Claude in my company repository, not in the
app's repository. The agent found the case study there and followed its link to
the published landing page. Then it checked `products/showcase/repos/`, a folder
of symlinks to the app repositories, and this app wasn't in it. Finally it ran a
`find` over the filesystem and located the project. Three tool calls, no
questions to me. I only noticed my mistake when I read its "found the code in…"
message.

**The honest answer to "are we sure?" was no.** The agent read the component,
the print CSS and the Android wrapper, and it didn't claim the feature works. It
said the code looks correct in a browser, that it had never been exercised, and
that there are two specific risks:

- **The Android build.** The app ships as a Capacitor APK. Inside an Android
  WebView, `window.print()` does nothing unless the native side hands it to
  `PrintManager`, and `MainActivity.java` has no such code. On my phone the button
  would most likely do nothing at all. This is the kind of bug you don't find by
  testing in desktop Chrome, which is where the feature was built.
- **Multi-page output.** While a modal is open, the page may have
  `overflow: hidden`, and Chrome sometimes prints only the first page. It
  can't be seen with a handful of boxes.

**The QR search I was looking for doesn't exist.** There is no scanner in the
app. The QR code on a label holds the app's ordinary deep link, `#box/<id>`, the
same link used for sharing a box. You point the phone's own camera at the label,
it opens the URL, and the app opens that box on load. That is a reasonable
design, and I had no idea it was the design. It has consequences the agent spelled
out: the link opens in the browser, not the installed app (there is no App Links
`intent-filter`), you need to be logged in there, and a label printed from
`localhost` during development encodes `localhost`.

**Testing without a printer.** In desktop Chrome, print to **Save as PDF**. Then
check that the PDF contains only the labels, 2 per row, none split across pages,
and all pages present with more than 12 boxes. Open the PDF on screen and scan
it with the phone. For layout alone, DevTools → Rendering → *Emulate CSS media
type: print* skips the dialog.

**What the agent did not do.** It didn't run the test. The app sits behind a
login, so generating the PDF would have meant authenticating a headless browser,
and I had asked a question, not ordered a test run. Every risk above is labeled
"likely" or "needs checking" for that reason, and I think that is the correct
wording. An answer that said "yes, it works" after reading the code would have
been worse than useless.

**A small snag at the end.** When I invoked `/blogworthy`, the export script
picked the right session but gave it an auto-generated title about a blog folder.
The prompt was also missing from the transcript, because it was written in VSCode,
not typed into the chat. The agent exported the session again under the prompt's
slug and put the prompt back at the top by hand.

## The pattern to steal

- **Question agent-built features before you describe them.** If you can't say
  how a feature works, you don't own it yet. Writing documentation or a case study
  is a good trigger for that audit.
- **Ask for a read-only answer with a clear boundary.** "Are we sure it works,
  and how would we test it" gets you an audit. "Make it work" gets you edits to
  code you haven't understood yet.
- **Make "looks right" and "was run" two separate claims.** Ask the agent to say which
  claims come from reading code and which from execution. Treat any "it works"
  without execution as a hypothesis.
- **Check every runtime the feature ships in.** Web APIs such as `window.print()`,
  file downloads and camera access behave differently inside WebViews. A feature
  built and checked in desktop Chrome can be dead in the APK.
- **Save as PDF is a free print test.** Emulated print media is an even cheaper
  one for layout.
- **A QR code on a physical object can just be a deep link.** You don't need an
  in-app scanner, as long as you know where that link opens and who has to be
  logged in there.
- **Don't fear starting in the wrong directory.** A capable agent will search the
  filesystem. It's still worth keeping a folder of symlinks to your working repos,
  and keeping it complete.

Next: actually running the PDF test, and deciding whether the Android build gets
native printing or simply hides the button.

<!-- DRAFT NOTES (remove before publishing):
- Run the Save-as-PDF test and add the result (screenshot of the label sheet?) before publishing.
- Confirm the Android no-op on a real device; the post currently says "most likely".
- products/showcase/repos/ lacks a StorageBoxOrganizer symlink; add it or drop that sentence.
- Asset idea: photo of a printed label on a real box.
-->
