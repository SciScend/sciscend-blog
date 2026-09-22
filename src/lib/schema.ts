import { SITE, BLOG_URL, asset } from '../site.config.ts';
import type { Post } from './posts.ts';

/** schema.org JSON-LD. Search engines and LLM agents read these to attribute posts. */

const abs = (path: string) => new URL(asset(path), SITE.origin).href;

export const publisher = {
  '@type': 'Organization',
  name: SITE.name,
  url: `${SITE.origin}/`,
  logo: { '@type': 'ImageObject', url: abs(SITE.logo) },
};

export const author = {
  '@type': 'Person',
  name: SITE.author.name,
  alternateName: SITE.author.nameEn,
  jobTitle: SITE.author.role,
  description: SITE.author.bio,
  worksFor: { '@type': 'Organization', name: SITE.name, url: `${SITE.origin}/` },
};

export function blogSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'Blog',
    name: SITE.title,
    description: SITE.description,
    url: BLOG_URL,
    inLanguage: SITE.lang,
    publisher,
    author,
  };
}

export function postSchema(post: Post, canonical: string) {
  const d = post.data;
  return {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: d.title,
    description: d.description,
    datePublished: d.pubDate.toISOString(),
    dateModified: (d.updatedDate ?? d.pubDate).toISOString(),
    inLanguage: d.lang,
    keywords: d.tags.join(', '),
    image: abs(d.heroImage ?? SITE.ogImage),
    url: canonical,
    mainEntityOfPage: { '@type': 'WebPage', '@id': canonical },
    isPartOf: { '@type': 'Blog', name: SITE.title, url: BLOG_URL },
    author,
    publisher,
  };
}
