// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

import { SITE } from './src/site.config.ts';

// Static output, served under https://sciscend.com/blog/. Built on the laptop and
// rsync'd to the VPS (see deploy/README.md). `site` + `base` together make every
// canonical URL, the sitemap and RSS absolute and correctly prefixed.
export default defineConfig({
  site: SITE.origin,
  base: SITE.base,
  output: 'static',
  trailingSlash: 'always',
  build: {
    // /blog/<slug>/index.html — clean URLs on nginx.
    format: 'directory',
  },
  markdown: {
    shikiConfig: { themes: { light: 'github-light', dark: 'github-dark' } },
  },
  integrations: [mdx(), sitemap()],
});
