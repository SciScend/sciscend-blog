#!/usr/bin/env node
/**
 * Print every tag used in src/content/blog with its post count, most used first.
 * Run before tagging a new post so existing tags get reused:  npm run tags
 * Drafts count too (a tag reserved by a draft is still a tag to reuse).
 */
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const ROOT = new URL('../src/content/blog/', import.meta.url).pathname;

function* files(dir) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) yield* files(p);
    else if (/\.mdx?$/.test(name)) yield p;
  }
}

/** Tags from the frontmatter: inline `tags: [a, b]` or a block list. */
function tagsOf(text) {
  const fm = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!fm) return [];
  const inline = fm[1].match(/^tags:\s*\[(.*)\]\s*$/m);
  if (inline) return inline[1].split(',').map(clean).filter(Boolean);
  const block = fm[1].match(/^tags:\s*\r?\n((?:\s+-.*\r?\n?)+)/m);
  if (block) return block[1].split('\n').map((l) => clean(l.replace(/^\s*-/, ''))).filter(Boolean);
  return [];
}
const clean = (s) => s.trim().replace(/^['"]|['"]$/g, '');

const counts = new Map();
for (const f of files(ROOT)) for (const t of tagsOf(readFileSync(f, 'utf8'))) counts.set(t, (counts.get(t) ?? 0) + 1);

const rows = [...counts].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
if (!rows.length) console.log('(no tags yet)');
for (const [tag, n] of rows) console.log(`${String(n).padStart(3)}  ${tag}`);
