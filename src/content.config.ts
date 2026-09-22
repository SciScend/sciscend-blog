import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

/**
 * Posts are Markdown/MDX files in src/content/blog/. The file path is the URL:
 *   src/content/blog/jev-test.md           → /blog/jev-test/
 *   src/content/blog/research/foo.md       → /blog/research/foo/
 *
 * Tags are the categories. They are not predefined: every tag used by a
 * published post gets its own page. The regex keeps them URL-safe and stops
 * near-duplicates like "LLMs" / "llm" from slipping in; reuse existing tags
 * (`npm run tags`) before inventing a new one.
 */
const TAG = z
  .string()
  .regex(/^[a-z0-9]+(-[a-z0-9]+)*$/, 'tags must be lowercase kebab-case, e.g. "model-tests"');

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    /** Meta description + share text. Aim for 120–160 characters. */
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    /** Language of this post's text. The blog UI stays Bulgarian. */
    lang: z.enum(['bg', 'en']).default('bg'),
    tags: z.array(TAG).default([]),
    /** Share image, relative to /public (e.g. "images/jev/cover.png"). */
    heroImage: z.string().optional(),
    /** Drafts are visible in `npm run dev`, never in a production build. */
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
