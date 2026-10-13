// Astro integration: after the build, every link to another site opens in a new
// tab. Links within sciscend.com (the blog, the portfolio, the placeholder),
// relative links, anchors and mailto: stay in the same tab.
//
// It rewrites the built HTML instead of hooking the Markdown pipeline, so it
// covers posts, news items and components alike, with no extra dependency.

import { readdir, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const OWN_HOSTS = new Set(['sciscend.com', 'www.sciscend.com']);

function isExternal(href) {
  if (!/^https?:\/\//i.test(href)) return false;
  try {
    return !OWN_HOSTS.has(new URL(href.replaceAll('&amp;', '&')).hostname);
  } catch {
    return false;
  }
}

export function markExternalLinks(html) {
  return html.replace(/<a\s[^>]*>/gi, (tag) => {
    const href = tag.match(/\shref="([^"]*)"/i)?.[1];
    if (!href || !isExternal(href) || /\starget=/i.test(tag)) return tag;
    const rel = tag.match(/\srel="([^"]*)"/i);
    if (rel) {
      const values = new Set(rel[1].split(/\s+/).filter(Boolean));
      values.add('noopener');
      tag = tag.replace(rel[0], ` rel="${[...values].join(' ')}"`);
    } else {
      tag = tag.replace(/>$/, ' rel="noopener">');
    }
    return tag.replace(/>$/, ' target="_blank">');
  });
}

async function* htmlFiles(dir) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) yield* htmlFiles(path);
    else if (entry.name.endsWith('.html')) yield path;
  }
}

export default function externalLinks() {
  return {
    name: 'external-links',
    hooks: {
      'astro:build:done': async ({ dir, logger }) => {
        let changed = 0;
        for await (const file of htmlFiles(fileURLToPath(dir))) {
          const html = await readFile(file, 'utf8');
          const out = markExternalLinks(html);
          if (out !== html) {
            await writeFile(file, out);
            changed++;
          }
        }
        logger.info(`off-site links set to open in a new tab in ${changed} page(s)`);
      },
    },
  };
}
