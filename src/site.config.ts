/**
 * Single source of truth for blog-wide metadata. Everything SEO/LLM-facing
 * (titles, JSON-LD, RSS, llms.txt, Open Graph) reads from here.
 *
 * Public text says "SciScend", never "SciScend ЕООД": nothing is registered yet.
 * The author wording follows company/iva-popova-bio-short.md in the SciScend
 * workspace — never "д-р" or "PhD".
 */

export const SITE = {
  /** Production origin — no trailing slash. */
  origin: 'https://sciscend.com',
  /** Path the blog is served under. Must match nginx `location ^~ /blog/`. */
  base: '/blog',

  name: 'SciScend',
  title: 'Блогът на SciScend',
  description:
    'Практичен AI, Python и машинно обучение на български: тестове на нови модели, ръководства за начинаещи и AI за малкия бизнес.',

  /** UI language of the blog. Each post also declares its own `lang`. */
  lang: 'bg',
  locale: 'bg_BG',

  /** Default share image, relative to /public. */
  ogImage: 'og-default.png',
  logo: 'logo.png',

  author: {
    name: 'Ива Попова',
    nameEn: 'Iva Popova',
    role: 'Основател на SciScend · обучител по Python, ML и AI',
    bio:
      'Ива Попова води курсове по Python, машинно обучение и AI от 2015 г., включително за корпоративни клиенти. ' +
      'Седем години преподава изкуствен интелект и езици за програмиране в ТУ–София, където прави и докторски изследвания в областта на семантичното търсене, онтологиите и NLP.',
  },

  contact: 'lab@sciscend.com',
} as const;

/** Absolute site URL for the blog root, with trailing slash. */
export const BLOG_URL = `${SITE.origin}${SITE.base}/`;

/** Build an internal blog path: url('tag/llm') → '/blog/tag/llm/'. */
export function url(path = ''): string {
  const clean = path.replace(/^\/+|\/+$/g, '');
  return clean ? `${SITE.base}/${clean}/` : `${SITE.base}/`;
}

/** Build a public file path (no trailing slash): asset('logo.png') → '/blog/logo.png'. */
export function asset(path: string): string {
  return `${SITE.base}/${path.replace(/^\/+/, '')}`;
}
