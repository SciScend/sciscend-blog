import type { APIRoute } from 'astro';
import { SITE, BLOG_URL } from '../site.config.ts';
import { getPosts } from '../lib/posts.ts';

/**
 * /blog/llms.txt — a plain Markdown index of the blog (llmstxt.org convention),
 * so LLM agents can find and cite posts without scraping HTML.
 */
export const GET: APIRoute = async () => {
  const posts = await getPosts();
  const lines = [
    `# ${SITE.title}`,
    '',
    `> ${SITE.description}`,
    '',
    `Автор: ${SITE.author.name} — ${SITE.author.role}. ${SITE.author.bio}`,
    `Статиите са на български, освен ако не е отбелязано друго. Контакт: ${SITE.contact}`,
    '',
    '## Статии',
    ...posts.map(
      (p) =>
        `- [${p.data.title}](${BLOG_URL}${p.id}/)${p.data.lang === 'en' ? ' (English)' : ''}: ${p.data.description}`,
    ),
    '',
  ];
  return new Response(lines.join('\n'), {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
};
