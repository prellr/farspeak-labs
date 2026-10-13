// Builds /sitemap.xml from every page in src/pages at build time.
// lastmod = git commit date of each page file (not the build time), so the
// IndexNow step only pings pages that actually changed.
import type { APIRoute } from 'astro';
import { execSync } from 'node:child_process';

const SITE = 'https://farspeaklabs.com';

function lastmod(file: string): string {
  try {
    const d = execSync(`git log -1 --format=%cs -- "${file}"`, { encoding: 'utf8' }).trim();
    if (d) return d;
  } catch {}
  return new Date().toISOString().slice(0, 10);
}

export const GET: APIRoute = () => {
  const pages = import.meta.glob('./**/*.{astro,md,mdx}', { eager: false });
  const urls = Object.keys(pages)
    .filter((p) => !p.includes('/_') && !p.includes('['))
    .map((p) => {
      const route = p.replace(/^\.\//, '').replace(/\.(astro|md|mdx)$/, '').replace(/(^|\/)index$/, '');
      const loc = `${SITE}/${route}${route ? '/' : ''}`;
      return `  <url><loc>${loc}</loc><lastmod>${lastmod('src/pages/' + p.slice(2))}</lastmod></url>`;
    })
    .sort();
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.join('\n')}\n</urlset>\n`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
};
