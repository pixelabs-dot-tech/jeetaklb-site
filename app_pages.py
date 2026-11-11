"""One link per app: jeetaklb.com/app (Jeetak, for customers), jeetaklb.com/partner (Jeetak Partner)
and jeetaklb.com/driver (Jeetak Driver).

Share these links instead of the store links. WhatsApp and other apps show the Jeetak
preview image set here (a store link only shows what the store decides), and the page
sends phones straight to the right store: Android to Google Play, iPhone to the App Store.
Computers see the page itself, with both store badges. Add ?stay to a link to see the
page on a phone.

build.py writes app.html, partner.html and driver.html, and draws their preview images
(og-app.jpg, og-partner.jpg, og-driver.jpg) with Playwright.
"""
import base64
import html as htmllib
import json
import os
from pathlib import Path

from pages import COMPANY, CSS as DOC_CSS, EMAIL, SITE_URL, nav_links

APPS = [
    {
        "slug": "app", "store": "customer", "name": "Jeetak",
        "kicker": "Jeetak app", "label": "",
        "title": "Get the Jeetak app", "og_title": ("Get the", "Jeetak app."),
        "page_title": "Get the Jeetak app · Everything you need",
        "accent": "Everything you need.",
        "lede": "Food, groceries and anything else from the shops near you, ordered in one app and "
                "delivered across 24 villages in the Upper Metn. No calls. No voice notes.",
        "desc": "Food, groceries and anything else from the shops near you, delivered across "
                "24 villages in the Upper Metn. Download the Jeetak app.",
        "policy": ("customer_policy", "privacy policy"),
        "art": "food", "art_bg": "orange", "og_theme": "orange", "og_art": "edge",
    },
    {
        "slug": "driver", "store": "driver", "name": "Jeetak Driver",
        "kicker": "Jeetak Driver app",
        "title": "Become a driver", "og_title": ("Become a", "Jeetak driver."),
        "accent": "Earn on every delivery.",
        "lede": "Deliver orders around the Upper Metn and earn on every delivery. "
                "The driver app shows your deliveries and earnings. Download it and apply from your phone.",
        "desc": "Deliver orders around the Upper Metn and earn on every delivery. "
                "Download the Jeetak Driver app and apply from your phone.",
        "policy": ("driver-policy", "driver policy"),
        "art": "scooter", "og_theme": "pine",
    },
    {
        "slug": "partner", "store": "vendor", "name": "Jeetak Partner",
        "kicker": "Jeetak Partner app",
        "title": "Become a partner", "og_title": ("Become a", "Jeetak partner."),
        "accent": "Get orders from 24 villages.",
        "lede": "Restaurants and shops: get orders from customers across 24 villages. "
                "Accept and prepare them in the Jeetak Partner app, and a Jeetak driver picks them up.",
        "desc": "Restaurants and shops: get orders from customers across 24 villages in the Upper Metn. "
                "Download the Jeetak Partner app and apply.",
        "policy": ("vendor-policy", "vendor policy"),
        "art": "shop", "og_theme": "orange",
    },
]

BADGE = {   # official store badges (symbols come from build.badge_symbols)
    "ios": ("badge-ios", 119.66407, 40, "Download on the App Store"),
    "android": ("badge-android", 564, 168, "Get it on Google Play"),
}
SOON = {"ios": "iPhone version coming soon.", "android": "Android version coming soon."}

# The shop and scooter drawings use the landing page's classes; these are the rules they need.
ART_CSS = """
.app-art, .og-art {
  --orange: #E23C0E; --orange-lit: #FF7A45; --orange-ink: #B32F0A; --pine: #1D3D2F; --pine-deep: #10241B;
  --cream: #FFFAE6; --stone: #EFE3C4; --glow: #FFD88A; --tree-fore: #0A1912; --white: #FFFFFF;
  --dough: #E9C27C; --herb: #7FAE4E; --kraft: #C99A5D; --kraft-dark: #A97C43;
  --dough-lite: #F3DBA6; --crust: #C98F45; --zaatar: #6B7433; --zaatar-dark: #454D1E; --herb-dark: #5C8A35;
  --melon: #F7A3A8; --water: #BFE6F4; --water-deep: #86C6E0; --tomato: #D9412F;
}
.c-dough { fill: var(--dough); } .c-crust { fill: var(--crust); } .c-zaatar { fill: var(--zaatar); }
.c-zaatar-dark { fill: var(--zaatar-dark); } .c-herb { fill: var(--herb); } .c-herb-dark { fill: var(--herb-dark); }
.c-cream { fill: var(--cream); } .c-pine { fill: var(--pine); } .c-melon { fill: var(--melon); }
.c-water { fill: var(--water); } .c-seed { fill: var(--pine-deep); } .c-tomato { fill: var(--tomato); }
.c-bag-lit { fill: var(--orange-lit); } .c-kraft-dark { fill: var(--kraft-dark); }
.ol { stroke: var(--pine-deep); stroke-width: 3; stroke-linejoin: round; stroke-linecap: round; }
.ln { fill: none; stroke: var(--pine-deep); stroke-width: 2.4; stroke-linecap: round; }
.ln-soft { opacity: 0.35; } .ln-water { stroke: var(--water-deep); } .ln-crust { stroke: var(--kraft-dark); }
.steam-line { fill: none; stroke: var(--cream); stroke-width: 3.2; stroke-linecap: round; opacity: 0.85; }
.app-art .steam-line { opacity: 0; animation: steam 2.8s ease-in-out infinite; transform-box: fill-box; }
.app-art .steam-line.s2 { animation-delay: 0.9s; }
@keyframes steam { 0% { opacity: 0; transform: translateY(8px); } 35% { opacity: 0.9; } 100% { opacity: 0; transform: translateY(-12px); } }
.pop { animation: pop 2.8s ease-in-out infinite; }
@keyframes pop { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }
.road-dots { fill: none; stroke: var(--orange-lit); stroke-width: 4; stroke-linecap: round; stroke-dasharray: 0.1 13; }
.road-dots.moving { animation: road 0.55s linear infinite; }
@keyframes road { to { stroke-dashoffset: 13; } }
.awning-a { fill: var(--orange); } .awning-b { fill: var(--cream); }
.c-stone { fill: var(--stone); } .c-door { fill: var(--pine-deep); } .win-on { fill: var(--glow); }
.c-bag { fill: var(--orange); } .c-white { fill: var(--white); } .c-can { fill: var(--orange-lit); }
.c-green { fill: var(--herb); } .c-jar { fill: var(--dough); } .c-kraft { fill: var(--kraft); }
.c-parapet, .crate-slat { fill: var(--kraft-dark); } .c-roof { fill: var(--orange); }
.shelf { fill: none; stroke: var(--stone); stroke-width: 2; }
.ticket { transform-box: fill-box; transform-origin: 50% 100%; animation: ticket 4s ease-in-out infinite; }
@keyframes ticket { 0%, 40% { transform: scale(0); } 48% { transform: scale(1.12); } 53%, 90% { transform: scale(1); } 100% { transform: scale(0); } }
.ticket-paper { fill: var(--cream); } .ticket-dot { fill: var(--orange-lit); }
.ticket-line { fill: none; stroke: var(--pine); stroke-width: 2.4; stroke-linecap: round; }
.speed { fill: none; stroke: var(--cream); stroke-width: 3; stroke-linecap: round; opacity: 0; animation: speed 1.1s linear infinite; }
.speed.sp2 { animation-delay: 0.35s; } .speed.sp3 { animation-delay: 0.7s; }
@keyframes speed { 0% { opacity: 0; transform: translateX(10px); } 30% { opacity: 0.7; } 100% { opacity: 0; transform: translateX(-14px); } }
.scoot { animation: scoot 0.5s ease-in-out infinite alternate; }
@keyframes scoot { from { transform: translateY(0); } to { transform: translateY(-1.6px); } }
.tire { fill: var(--tree-fore); }
.spokes { transform-box: fill-box; transform-origin: center; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.spoke { fill: none; stroke: var(--stone); stroke-width: 2; stroke-linecap: round; opacity: 0.6; }
.scoot-body { fill: var(--cream); } .scoot-dark { fill: var(--pine-deep); }
.scoot-line { fill: none; stroke: var(--cream); stroke-width: 5; stroke-linecap: round; }
.scoot-bar { fill: none; stroke: var(--pine-deep); stroke-width: 4; stroke-linecap: round; }
.rack { fill: none; stroke: var(--pine-deep); stroke-width: 3; stroke-linecap: round; }
.bag-seam { fill: none; stroke: var(--orange-ink); stroke-width: 2.5; }
@media (prefers-reduced-motion: reduce) {
  .app-art * { animation: none !important; }
  .app-art .speed { opacity: 0.5; }
  .app-art .steam-line { opacity: 0.85; }
}
"""

APP_CSS = """
.app-page { min-height: 100vh; min-height: 100svh; display: flex; flex-direction: column; }
.app-page > main { flex: 1 0 auto; display: flex; align-items: center; }
.app-page > main > .app { width: 100%; }
.app-wrap { max-width: 64rem; }
.app { padding-block: clamp(2rem, 6vw, 3.5rem) clamp(3rem, 8vw, 4.5rem); }
.app-grid { display: grid; gap: clamp(1.5rem, 4vw, 2.75rem); align-items: center; }
@media (min-width: 760px) {
  .app-grid { grid-template-columns: 1fr 1.05fr; }
  .app-art { order: 2; }
}
.app-accent {
  margin: 0.4rem 0 0;
  font-family: var(--font-display);
  font-style: italic;
  font-weight: 700;
  font-size: clamp(1.35rem, 4.2vw, 1.85rem);
  line-height: 1.15;
  color: var(--orange-ink);
}
.app-art { margin: 0; background: var(--pine); border-radius: 22px; overflow: hidden; aspect-ratio: 12 / 7; }
.app-art.is-orange { background: var(--orange); }
.app-art > svg { display: block; width: 100%; height: 100%; }
.app-lede { margin: 1.1rem 0 0; font-size: 1.0625rem; max-width: 34rem; }
.app-stores { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 1.5rem; }
.app-store { display: inline-block; line-height: 0; border-radius: 9px; }
.app-store svg { display: block; height: 2.875rem; width: auto; }
.app-note { margin: 0.8rem 0 0; font-size: 0.9375rem; color: var(--ink-soft); }
.app-more { margin: 1.75rem 0 0; font-size: 0.9375rem; color: var(--ink-soft); }
.app-more a { color: var(--orange-ink); text-decoration-thickness: 1.5px; text-underline-offset: 3px; }
"""


def esc(t):
    return htmllib.escape(t, quote=True)


def badges(links, height_css=None):
    out = []
    for key in ("ios", "android"):
        url = links.get(key)
        if not url:
            continue
        symbol, w, h, label = BADGE[key]
        out.append(f'<a class="app-store" href="{esc(url)}" aria-label="{label}">'
                   f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true" focusable="false">'
                   f'<use href="#{symbol}"/></svg></a>')
    return "".join(out)


def missing_note(links):
    gone = [k for k in ("ios", "android") if not links.get(k)]
    return SOON[gone[0]] if len(gone) == 1 else ""


# The customer app's picture: food from the landing page's footer, popping up from the bottom edge.
# (name, centre x, bottom y, scale, tilt) in a 240 x 140 box; anything below 140 is cut off.
FOOD_SPREAD = [("groceries", 41, 150, 1.18, -7), ("coffee", 98, 146, 1.16, 5), ("shawarma", 152, 152, 1.18, -4),
               ("booza", 201, 148, 1.16, 5), ("manoushe", 137, 171, 0.8, -6)]
FOOD_BOX = {"manoushe": (2.6, 106.2, 98.3), "shawarma": (28, 101, 72.1), "coffee": (27, 101, 73), "booza": (26.8, 102, 73.2),
            "groceries": (25, 102, 75)}      # each drawing's left edge, bottom and right edge in its 100 x 100 box


def food_svg(pin_w, pin_h):
    from food_items import FOOD
    drawings = {name: inner.replace("{PIN_W}", str(pin_w)).replace("{PIN_H}", str(pin_h)) for name, inner in FOOD}
    out = []
    for i, (name, cx, bottom, scale, tilt) in enumerate(FOOD_SPREAD):
        left, low, right = FOOD_BOX[name]
        out.append(f'<g class="pop" style="animation-delay:{-0.55 * i:.2f}s"><g transform="translate({cx} {bottom}) '
                   f'rotate({tilt}) scale({scale}) translate({-(left + right) / 2:.1f} {-low})">{drawings[name]}</g></g>')
    return f'<svg viewBox="0 0 240 140" focusable="false">{"".join(out)}</svg>'


def render(site_dir, word_d, wm_w, wm_h, font_links, store_links, art, badge_symbols, extra_defs=""):
    """Write app.html, driver.html and partner.html. art maps "food"/"scooter"/"shop" to inline SVG markup."""
    written = []
    for a in APPS:
        links = store_links[a["store"]]
        title = f'{a["og_title"][0]} {a["og_title"][1]}'.replace(".", "")
        page_title = a.get("page_title") or f'{a["name"]} app · {title}'
        url = f"{SITE_URL}/{a['slug']}"
        redirect = json.dumps({"ios": links.get("ios", ""), "android": links.get("android", "")})
        note = missing_note(links)
        policy_slug, policy_label = a["policy"]
        page = f"""<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(page_title)}</title>
<meta name="description" content="{esc(a['desc'])}">
<meta name="theme-color" content="#1D3D2F">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Jeetak">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(page_title)}">
<meta property="og:description" content="{esc(a['desc'])}">
<meta property="og:image" content="{SITE_URL}/og-{a['slug']}.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(a['name'])}: {esc(title)}">
<meta name="twitter:card" content="summary_large_image">
<script>
  // Phones go straight to their store (link previews don't run this, so they read the tags above).
  (function () {{
    var links = {redirect};
    if (/[?&]stay\\b/.test(location.search)) return;
    var ua = navigator.userAgent || "";
    var ios = /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
    var target = /Android/i.test(ua) ? links.android : (ios ? links.ios : "");
    if (target) location.replace(target);
  }})();
</script>
{font_links}
<style>{DOC_CSS}{ART_CSS}{APP_CSS}</style>
</head>
<body class="app-page">
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <defs>
    <path id="jk-word" fill-rule="evenodd" d="{word_d}"/>{extra_defs}
    {badge_symbols}
  </defs>
</svg>
<header class="doc-top">
  <div class="doc-wrap app-wrap doc-top-row">
    <a class="brand" href="/" aria-label="Jeetak home"><svg class="wordmark" viewBox="0 0 {wm_w} {wm_h}" aria-hidden="true" focusable="false"><use href="#jk-word"/></svg></a>
    <a class="doc-home" href="/">Home</a>
  </div>
</header>
<main class="doc-wrap app-wrap">
  <article class="doc app">
    <div class="app-grid">
      <figure class="app-art{' is-orange' if a.get('art_bg') == 'orange' else ''}" aria-hidden="true">{art[a['art']]}</figure>
      <div class="app-copy">
        <p class="doc-kicker">{esc(a['kicker'])}</p>
        <h1>{esc(a['title'])}</h1>
        <p class="app-accent">{esc(a['accent'])}</p>
        <p class="app-lede">{esc(a['lede'])}</p>
        <div class="app-stores">{badges(links)}</div>
        {f'<p class="app-note">{note}</p>' if note else ''}
        <p class="app-more">Read the <a href="/{policy_slug}">{policy_label}</a>. Questions? <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
    </div>
  </article>
</main>
<footer class="doc-foot">
  <div class="doc-wrap app-wrap">
    <nav class="doc-links" aria-label="Jeetak pages">{nav_links()}</nav>
    <p class="doc-meta">© 2026 {COMPANY} · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  </div>
</footer>
</body>
</html>
"""
        path = site_dir / f"{a['slug']}.html"
        path.write_text(page)
        written.append(path.name)
    return written


# ---------------------------------------------------------------- link preview images
OG_THEMES = {
    "pine": {"bg": "#1D3D2F", "word": "#FFFAE6", "label": "#FF7A45", "kicker": "#FF7A45",
             "title": "#FFFAE6", "accent": "#FF7A45", "soon": "#D6DCC8"},
    "orange": {"bg": "#E23C0E", "word": "#FFFFFF", "label": "#10241B", "kicker": "#10241B",
               "title": "#FFFFFF", "accent": "#10241B", "soon": "#10241B"},
}


def og_html(a, word_d, wm_w, wm_h, art, badge_symbols, store_links, font_css, extra_defs=""):
    t = OG_THEMES[a["og_theme"]]
    links = store_links[a["store"]]
    note = missing_note(links)
    label = a.get("label", a["name"].split()[-1])    # "Driver" / "Partner"; none for the customer app
    # the shop's orange awning needs a pine card on orange; the food pops up from the bottom edge
    mode = a.get("og_art") or ("panel" if a["og_theme"] != "pine" else "bare")
    art_svg = art[a["art"]]
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{font_css}
{ART_CSS}
html, body {{ margin: 0; }}
body {{ width: 1200px; height: 630px; overflow: hidden; background: {t['bg']}; font-family: "Readex Pro", sans-serif; }}
.og {{ position: relative; width: 1200px; height: 630px; box-sizing: border-box; padding: 60px 70px; }}
.og * {{ animation: none !important; }}
.og .speed {{ opacity: 0.6; }}
.brandrow {{ display: flex; align-items: flex-end; gap: 16px; }}
.brandrow svg {{ display: block; height: 52px; width: auto; fill: {t['word']}; }}
.brandrow span {{ font-family: "Kanit"; font-style: italic; font-weight: 600; font-size: 36px; line-height: 1; color: {t['label']}; padding-bottom: 2px; }}
.kicker {{ margin: 54px 0 0; display: flex; align-items: center; gap: 14px; font-weight: 600; font-size: 21px; letter-spacing: 0.16em; text-transform: uppercase; color: {t['kicker']}; }}
.kicker::before {{ content: ""; width: 42px; border-top: 6px dotted {t['kicker']}; }}
h1 {{ margin: 16px 0 0; font-family: "Kanit"; font-style: italic; font-weight: 700; font-size: 84px; line-height: 0.98; letter-spacing: -0.01em; color: {t['title']}; }}
.accent {{ margin: 14px 0 0; font-family: "Kanit"; font-style: italic; font-weight: 700; font-size: 40px; line-height: 1.05; color: {t['accent']}; }}
.stores {{ position: absolute; left: 70px; bottom: 56px; display: flex; align-items: center; gap: 14px; }}
.stores a {{ display: block; line-height: 0; }}
.stores svg {{ display: block; height: 60px; width: auto; }}
.soon {{ margin-left: 6px; font-weight: 500; font-size: 19px; color: {t['soon']}; }}
.og-art {{ position: absolute; right: 50px; width: 540px; }}
.og-art > svg {{ display: block; width: 100%; height: auto; }}
.og-art.is-bare {{ bottom: 60px; }}
.og-art.is-edge {{ bottom: 0; right: 20px; width: 650px; }}
.og .steam-line {{ opacity: 0.85; }}
.og-art.is-panel {{ top: 132px; right: 46px; width: 442px; padding: 0; border-radius: 26px; overflow: hidden; background: #1D3D2F;
  transform: rotate(-2.5deg); box-shadow: 0 22px 44px rgba(16, 36, 27, 0.35); }}
</style></head><body>
<svg width="0" height="0" style="position:absolute"><defs><path id="jk-word" fill-rule="evenodd" d="{word_d}"/>{extra_defs}{badge_symbols}</defs></svg>
<div class="og">
  <div class="brandrow"><svg viewBox="0 0 {wm_w} {wm_h}"><use href="#jk-word"/></svg>{f'<span>{esc(label)}</span>' if label else ''}</div>
  <p class="kicker">{esc(a['kicker'])}</p>
  <h1>{esc(a['og_title'][0])}<br>{esc(a['og_title'][1])}</h1>
  <p class="accent">{esc(a['accent'])}</p>
  <div class="stores">{badges(links)}{f'<span class="soon">{note}</span>' if note else ''}</div>
  <div class="og-art is-{mode}">{art_svg}</div>
</div>
</body></html>"""


# Fonts for the preview images. Normally they load from Google Fonts; where that is blocked,
# point JEETAK_FONTS at a node_modules/@fontsource folder (npm i @fontsource/kanit @fontsource/readex-pro).
LOCAL_FONTS = [("Kanit", "italic", 600, "kanit/files/kanit-latin-600-italic.woff2"),
               ("Kanit", "italic", 700, "kanit/files/kanit-latin-700-italic.woff2"),
               ("Readex Pro", "normal", 500, "readex-pro/files/readex-pro-latin-500-normal.woff2"),
               ("Readex Pro", "normal", 600, "readex-pro/files/readex-pro-latin-600-normal.woff2")]


def og_font_css(fonts_url):
    root = os.environ.get("JEETAK_FONTS")
    if not root:
        return f'@import url("{fonts_url}");'
    rules = []
    for family, style, weight, rel in LOCAL_FONTS:
        data = base64.b64encode((Path(root) / rel).read_bytes()).decode()
        rules.append(f'@font-face {{ font-family: "{family}"; font-style: {style}; font-weight: {weight}; '
                     f'src: url(data:font/woff2;base64,{data}) format("woff2"); }}')
    return "\n".join(rules)
