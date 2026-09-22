import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { SITE, url } from '../site.config.ts';
import { getPosts } from '../lib/posts.ts';

export async function GET(context: APIContext) {
  const posts = await getPosts();
  return rss({
    title: SITE.title,
    description: SITE.description,
    site: context.site!,
    customData: `<language>${SITE.lang}</language>`,
    items: posts.map((p) => ({
      title: p.data.title,
      description: p.data.description,
      pubDate: p.data.pubDate,
      link: url(p.id),
      categories: p.data.tags,
    })),
  });
}
