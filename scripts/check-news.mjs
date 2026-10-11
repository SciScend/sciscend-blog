#!/usr/bin/env node
/**
 * Check that every news item (src/content/blog/novini/*.md) follows the news
 * format, so the section reads the same whatever the item started from (a
 * LinkedIn post or a blank page):  npm run check:news
 *
 * Runs before every build. Problems in a published item fail the build; in a
 * draft they are only reported, so a work-in-progress draft never blocks a
 * deploy. The rules are described in the /blog-post skill, "News format".
 */
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const ROOT = new URL('../', import.meta.url).pathname;
const DIR = join(ROOT, 'src/content/blog/novini');

const WORDS = { min: 100, max: 300 };
const TAGS = { min: 2, max: 4 };
const DESCRIPTION = { min: 120, max: 160 };
const TITLE_MAX = 70;
const SLUG = /^[a-z0-9]+(-[a-z0-9]+)*$/;
const SLUG_MAX = 40;
/** Leftovers of a LinkedIn post that mean nothing on the blog. */
const LINKEDIN = [/първия коментар/i, /first comment/i, /see more/i];

/** Frontmatter as { key: raw string value }, plus the body. Single-line values only. */
function parse(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
  if (!m) return null;
  const fm = {};
  for (const line of m[1].split(/\r?\n/)) {
    const kv = line.match(/^([A-Za-z]+):\s*(.*)$/);
    if (kv) fm[kv[1]] = kv[2].trim();
  }
  return { fm, body: m[2] };
}

/** Unquote a YAML scalar: 'it''s' -> it's, "x" -> x. */
function scalar(v = '') {
  if (/^'.*'$/.test(v)) return v.slice(1, -1).replace(/''/g, "'");
  if (/^".*"$/.test(v)) return v.slice(1, -1).replace(/\\"/g, '"');
  return v;
}

function check(file) {
  const problems = [];
  const slug = file.replace(/\.mdx?$/, '');
  const doc = parse(readFileSync(join(DIR, file), 'utf8'));
  if (!doc) return { draft: false, problems: ['no frontmatter'] };
  const { fm, body } = doc;

  if (!SLUG.test(slug) || slug.length > SLUG_MAX)
    problems.push(`slug "${slug}": Latin kebab-case, at most ${SLUG_MAX} characters`);

  const title = scalar(fm.title);
  if (!title) problems.push('title is missing');
  else if ([...title].length > TITLE_MAX) problems.push(`title is ${[...title].length} characters (max ${TITLE_MAX})`);

  const description = scalar(fm.description);
  const dlen = [...description].length;
  if (dlen < DESCRIPTION.min || dlen > DESCRIPTION.max)
    problems.push(`description is ${dlen} characters (${DESCRIPTION.min}-${DESCRIPTION.max})`);

  const tags = (fm.tags?.match(/^\[(.*)\]$/)?.[1] ?? '').split(',').map((t) => scalar(t.trim())).filter(Boolean);
  if (tags.length < TAGS.min || tags.length > TAGS.max)
    problems.push(`${tags.length} tags (${TAGS.min}-${TAGS.max}, inline list: tags: [a, b])`);

  const hero = scalar(fm.heroImage);
  if (hero && !existsSync(join(ROOT, 'public', hero))) problems.push(`heroImage public/${hero} does not exist`);

  const prose = body.replace(/```[\s\S]*?```/g, '');
  const words = prose
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/https?:\/\/\S+/g, '')
    .split(/\s+/)
    .filter((w) => /[\p{L}\p{N}]/u.test(w)).length;
  if (words < WORDS.min || words > WORDS.max) problems.push(`${words} words (${WORDS.min}-${WORDS.max})`);

  if (!/\]\(https?:\/\/[^)]+\)|<https?:\/\/[^>]+>/.test(prose))
    problems.push('no link to the source in the text');

  if (/^#{1,6}\s/m.test(prose)) problems.push('headings: a news item is plain paragraphs, no ## sections');

  const hashtags = prose.match(/(^|\s)#[\p{L}][\p{L}\p{N}_]*/gu);
  if (hashtags) problems.push(`hashtags in the text (${hashtags.map((h) => h.trim()).join(' ')}): use tags instead`);

  for (const re of LINKEDIN) if (re.test(prose)) problems.push(`LinkedIn leftover: "${prose.match(re)[0]}"`);

  return { draft: scalar(fm.draft) === 'true', problems };
}

if (!existsSync(DIR)) process.exit(0);

let failed = false;
for (const file of readdirSync(DIR).filter((f) => /\.mdx?$/.test(f)).sort()) {
  const { draft, problems } = check(file);
  if (!problems.length) continue;
  const label = draft ? 'warning (draft)' : 'error';
  console.log(`novini/${file}: ${label}`);
  for (const p of problems) console.log(`  - ${p}`);
  if (!draft) failed = true;
}
if (failed) {
  console.log('\nNews format check failed: fix the items above (rules: /blog-post skill, "News format").');
  process.exit(1);
}
