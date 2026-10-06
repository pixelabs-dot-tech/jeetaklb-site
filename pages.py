"""Render the policy pages (about-us, terms, customer_policy, vendor-policy, driver-policy,
account-deletion) as standalone HTML files next to index.html."""
import html as htmllib

import markdown

from pages_text import PAGES, UPDATED

EMAIL = "support@jeetaklb.com"
COMPANY = "Jeetak SARL"
SITE_URL = "https://jeetaklb.com"

CSS = """
:root {
  --orange: #E23C0E;
  --orange-lit: #FF7A45;
  --orange-ink: #B32F0A;
  --pine: #1D3D2F;
  --pine-deep: #10241B;
  --cream: #FFFAE6;
  --cream-dim: #D6DCC8;
  --ink: #15271E;
  --ink-soft: #4A5D52;
  --font-display: "Kanit", "Readex Pro", system-ui, sans-serif;
  --font-body: "Readex Pro", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-ar: "Baloo Bhaijaan 2", "Readex Pro", "Geeza Pro", "Noto Sans Arabic", sans-serif;
  color-scheme: light;
  background: var(--pine);
}
*, *::before, *::after { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--cream);
  color: var(--ink);
  font-family: var(--font-body);
  font-size: 1rem;
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
  -webkit-text-size-adjust: 100%;
}
.doc-wrap { width: 100%; max-width: 46rem; margin-inline: auto; padding-inline: clamp(1.25rem, 4vw, 2rem); }
:focus-visible { outline: 3px solid var(--orange-ink); outline-offset: 3px; border-radius: 4px; }
.doc-top :focus-visible, .doc-foot :focus-visible { outline-color: var(--orange-lit); }

.doc-top { background: var(--pine); color: var(--cream); padding-top: env(safe-area-inset-top, 0px); }
.doc-top-row { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding-block: 1.1rem; }
.brand { display: block; line-height: 0; }
.wordmark { display: block; width: 7.25rem; height: auto; fill: var(--cream); }
.doc-home {
  color: var(--cream);
  text-decoration: none;
  font-size: 0.9375rem;
  font-weight: 500;
  border-bottom: 2px dotted var(--orange-lit);
}
.doc-home:hover { border-bottom-style: solid; }

.doc { padding-block: clamp(2.25rem, 6vw, 3.5rem) clamp(3rem, 8vw, 4.5rem); }
.doc-kicker {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin: 0 0 0.75rem;
  font-size: 0.8125rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--orange-ink);
}
.doc-kicker::before { content: ""; width: 1.6rem; border-top: 4px dotted var(--orange); }
.doc h1 {
  margin: 0;
  font-family: var(--font-display);
  font-style: italic;
  font-weight: 700;
  font-size: clamp(2.1rem, 6.5vw, 3.1rem);
  line-height: 1.05;
  letter-spacing: -0.01em;
  text-wrap: balance;
}
.doc-date { margin: 0.85rem 0 2rem; color: var(--ink-soft); font-size: 0.9375rem; }
.doc h2 {
  margin: 2.25rem 0 0.5rem;
  font-family: var(--font-display);
  font-style: italic;
  font-weight: 600;
  font-size: clamp(1.3rem, 3.6vw, 1.6rem);
  line-height: 1.2;
  color: var(--pine);
  text-wrap: balance;
}
.doc p, .doc li { max-width: 68ch; }
.doc p { margin: 0.75rem 0; }
.doc ul, .doc ol { margin: 0.6rem 0 1rem; padding-inline-start: 1.35rem; }
.doc li { margin: 0.35rem 0; padding-inline-start: 0.2rem; }
.doc ul li::marker { color: var(--orange); }
.doc ol li::marker { color: var(--orange-ink); font-weight: 700; }
.doc a { color: var(--orange-ink); text-decoration-thickness: 1.5px; text-underline-offset: 3px; }
.doc strong { font-weight: 600; }

.doc-villages {
  list-style: none;
  margin: 1rem 0 0;
  padding: 0 !important;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(9rem, 1fr));
  gap: 0.5rem;
}
.doc-villages li {
  margin: 0;
  padding: 0.55rem 0.7rem;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.05rem;
  border-radius: 7px;
  background: var(--pine);
  color: var(--cream);
  line-height: 1.25;
}
.doc-villages li::marker { content: none; }
.v-ar { font-family: var(--font-ar); font-size: 1.05rem; font-weight: 600; }
.v-lat { font-size: 0.75rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; }

.doc-foot { background: var(--pine); color: var(--cream-dim); padding-bottom: env(safe-area-inset-bottom, 0px); }
.doc-foot .doc-wrap { display: grid; gap: 1rem; padding-block: 1.75rem 2rem; }
.doc-links { display: flex; flex-wrap: wrap; gap: 0.45rem 1.25rem; }
.doc-links a { color: var(--cream); font-size: 0.9375rem; font-weight: 500; text-decoration: none; }
.doc-links a:hover { text-decoration: underline; }
.doc-links a[aria-current="page"] { color: var(--orange-lit); }
.doc-meta { margin: 0; font-size: 0.875rem; }
.doc-meta a { color: var(--cream-dim); }
"""


def nav_links(current=None):
    """Links to every policy page, for the footers."""
    out = []
    for slug, _title, label, *_ in PAGES:
        cur = ' aria-current="page"' if slug == current else ""
        out.append(f'<a href="/{slug}"{cur}>{htmllib.escape(label)}</a>')
    return "".join(out)


def render(site_dir, word_d, wm_w, wm_h, font_links, villages):
    village_items = "".join(
        f'<li><span class="v-ar" lang="ar">{ar}</span><span class="v-lat">{htmllib.escape(lat)}</span></li>'
        for lat, ar in villages)
    written = []
    for slug, title, _label, kicker, desc, text in PAGES:
        md = (text.replace("{EMAIL}", EMAIL).replace("{COMPANY}", COMPANY)
              .replace("{HOME}", "").replace("{VILLAGES}", village_items))
        body = markdown.markdown(md, extensions=["extra", "sane_lists"], output_format="html")
        t = htmllib.escape(title)
        d = htmllib.escape(desc)
        page = f"""<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t} · Jeetak</title>
<meta name="description" content="{d}">
<meta name="theme-color" content="#1D3D2F">
<link rel="canonical" href="{SITE_URL}/{slug}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Jeetak">
<meta property="og:url" content="{SITE_URL}/{slug}">
<meta property="og:title" content="{t} · Jeetak">
<meta property="og:description" content="{d}">
<meta property="og:image" content="{SITE_URL}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
{font_links}
<style>{CSS}</style>
</head>
<body>
<header class="doc-top">
  <div class="doc-wrap doc-top-row">
    <a class="brand" href="/" aria-label="Jeetak home"><svg class="wordmark" viewBox="0 0 {wm_w} {wm_h}" aria-hidden="true" focusable="false"><path fill-rule="evenodd" d="{word_d}"/></svg></a>
    <a class="doc-home" href="/">Home</a>
  </div>
</header>
<main class="doc-wrap">
  <article class="doc">
    <p class="doc-kicker">{htmllib.escape(kicker)}</p>
    <h1>{t}</h1>
    <p class="doc-date">Last updated {UPDATED}</p>
{body}
  </article>
</main>
<footer class="doc-foot">
  <div class="doc-wrap">
    <nav class="doc-links" aria-label="Jeetak pages">{nav_links(slug)}</nav>
    <p class="doc-meta">© 2026 {COMPANY} · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  </div>
</footer>
</body>
</html>
"""
        path = site_dir / f"{slug}.html"
        path.write_text(page)
        written.append(path.name)
    return written
