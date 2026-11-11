"""Build the redesign of the landing page (a preview; the live site is still built by ../build.py).

  python3 revamp/build.py

writes out/revamp.html (the page without its document wrapper, for the Claude artifact preview)
and out/revamp-site/index.html (the same page as a deployable file).

It reuses the live site's data: the store links and the copy (src/script.js), the store badges
(src/), the footer food drawings (food_items.py) and the map drawing code (village_map.py).
Its own files are in this folder: body.html, style.css, script.js and assets/.
"""
import base64
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = ROOT / "src"
OUT = ROOT / "out"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

FONTS = ("https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900"
         "&family=Saira:ital,wght@1,800;1,900&display=swap")

# ---------------------------------------------------------------- the real logo, from the brand guide
BRAND = json.loads((HERE / "assets" / "brand_logo.json").read_text())
WORDMARK, LOCKUP = BRAND["logo"]["wordmark"], BRAND["logo"]["ar"]
PIN_D, PIN_W, PIN_H = BRAND["pin"], 178.5, 226.3


def logo_symbol(symbol_id, lock):
    """One <symbol> per lockup. Each part (the j, its pin, the word, the tagline) keeps its own class,
    so a colourway is only a few CSS variables: see .logo--white in style.css."""
    paths = "".join(f'<path class="lg-{part}" fill-rule="evenodd" d="{d}"/>' for part, d in lock["paths"].items())
    return f'<symbol id="{symbol_id}" viewBox="0 0 {lock["w"]} {lock["h"]}">{paths}</symbol>'


LOGO_SYMBOLS = logo_symbol("jk-wordmark", WORDMARK) + "\n    " + logo_symbol("jk-lockup", LOCKUP)
BAG_LOGO = (f'<svg class="logo--white" x="12" y="40.5" width="30" height="10.8" viewBox="0 0 {WORDMARK["w"]} {WORDMARK["h"]}">'
            f'<use href="#jk-wordmark"/></svg>')

# ---------------------------------------------------------------- store badges and links (from the live site)
LIVE_JS = (SRC / "script.js").read_text()
STORE_LINKS_JS = re.search(r"(  var STORE_LINKS = \{.*?\n  \};)", LIVE_JS, re.S).group(1)
T_BASE_JS = re.search(r"(  var T = \{.*?\n  \};)\n\n  var root", LIVE_JS, re.S).group(1)
STORE_LINKS = {app: {"ios": ios, "android": android} for app, ios, android in re.findall(
    r'(customer|vendor|driver):\s*\{ ios: "([^"]*)", android: "([^"]*)" \}', LIVE_JS)}
assert set(STORE_LINKS) == {"customer", "vendor", "driver"}, STORE_LINKS

BADGES = {
    "ios": ("badge-ios", 119.66407, 40, "Download on the App Store"),
    "android": ("badge-android", 564, 168, "Get it on Google Play"),
}


def badge_symbols():
    art = (SRC / "badge-app-store.svg").read_text()
    art = art[art.index(">") + 1:art.rindex("</svg>")]
    art = re.sub(r'<title>.*?</title>|\s+(?:id|data-name)="[^"]*"', "", art, flags=re.S).strip()
    png = base64.b64encode((SRC / "badge-google-play.png").read_bytes()).decode()
    return (f'<symbol id="badge-ios" viewBox="0 0 119.66407 40">{art}</symbol>\n'
            f'    <symbol id="badge-android" viewBox="0 0 564 168"><image href="data:image/png;base64,{png}" '
            f'width="564" height="168"/></symbol>')


def store(app, key):
    symbol, w, h, label = BADGES[key]
    url = STORE_LINKS[app][key]
    link = f'class="store" href="{url}" target="_blank" rel="noopener"' if url else 'class="store is-soon"'
    return (f'<a {link} data-app="{app}" data-store="{key}" aria-label="{label}">'
            f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true" focusable="false">'
            f'<use href="#{symbol}"/></svg></a>')


# ---------------------------------------------------------------- drawings
def shop_svg():
    stripes = "".join(
        f'<path class="{"awning-a" if i % 2 == 0 else "awning-b"}" d="M{40 + 18 * i} 40 H{58 + 18 * i} V56 A9 9 0 0 1 {40 + 18 * i} 56 Z"/>'
        for i in range(8))
    goods = []
    for shelf_y, kinds in ((84, "jcgjcg"), (97, "cgjcgj"), (110, "gjcgjc")):
        for j, kind in enumerate(kinds):
            x = 62 + 9.4 * j
            if kind == "j":
                goods.append(f'<rect class="c-jar" x="{x:.1f}" y="{shelf_y - 9}" width="6.5" height="9" rx="1.5"/>')
            elif kind == "c":
                goods.append(f'<rect class="c-can" x="{x:.1f}" y="{shelf_y - 7}" width="6.5" height="7" rx="1"/>')
            else:
                goods.append(f'<circle class="c-green" cx="{x + 3.2:.1f}" cy="{shelf_y - 4}" r="4"/>')
    return f"""<svg viewBox="0 0 240 128" focusable="false">
              <path class="road-dots" d="M6 119 H234"/>
              <g transform="translate(0 -12)">
              <rect class="c-stone" x="46" y="34" width="132" height="90"/>
              <rect class="c-parapet" x="40" y="26" width="144" height="10" rx="2"/>
              {stripes}
              <rect class="c-door" x="58" y="70" width="62" height="40"/>
              <path class="shelf" d="M58 84 H120 M58 97 H120"/>
              {"".join(goods)}
              <rect class="c-door" x="134" y="70" width="32" height="54"/>
              <path class="shelf" d="M146 70 L150 78 L154 70"/>
              <rect class="ticket-paper" x="141" y="78" width="18" height="10" rx="2"/>
              <circle class="c-stone" cx="160" cy="100" r="2"/>
              <circle class="c-can" cx="194" cy="103" r="5"/>
              <circle class="c-roof" cx="204" cy="101.5" r="5"/>
              <circle class="c-green" cx="214" cy="103" r="5"/>
              <rect class="c-kraft" x="186" y="105" width="38" height="19" rx="2"/>
              <rect class="crate-slat" x="186" y="112" width="38" height="3"/>
              <g class="ticket">
                <path class="ticket-paper" d="M192 26 H216 V54 L210 50 L204 54 L198 50 L192 54 Z"/>
                <path class="ticket-line" d="M197 33 H211 M197 39 H211 M197 45 H206"/>
                <circle class="ticket-dot" cx="216" cy="26" r="5"/>
              </g>
              </g>
            </svg>"""


SCOOTER_PARTS = f"""<circle class="tire" cx="40" cy="96" r="15"/>
                  <g class="spokes"><path class="spoke" d="M31 96 H49 M35.5 88.2 L44.5 103.8 M35.5 103.8 L44.5 88.2"/></g>
                  <circle class="c-stone" cx="40" cy="96" r="5"/>
                  <circle class="tire" cx="138" cy="96" r="15"/>
                  <g class="spokes"><path class="spoke" d="M129 96 H147 M133.5 88.2 L142.5 103.8 M133.5 103.8 L142.5 88.2"/></g>
                  <circle class="c-stone" cx="138" cy="96" r="5"/>
                  <path class="rack" d="M10 60 H46"/>
                  <rect class="c-bag" x="8" y="22" width="38" height="36" rx="5"/>
                  <path class="bag-seam" d="M8 34 H46"/>
                  <g class="bag-logo">{BAG_LOGO}</g>
                  <path class="scoot-body" d="M14 88 C12 74 22 62 38 60 H82 C88 60 92 64 92 70 V88 H62 C60 78 52 72 40 72 C28 72 20 78 18 88 Z"/>
                  <path class="scoot-dark" d="M42 60 C42 54 46 51 52 51 H80 C86 51 88 55 88 60 Z"/>
                  <path class="scoot-body" d="M90 82 H122 C124 82 125 84 125 86 V90 H90 Z"/>
                  <path class="scoot-body" d="M118 90 C122 78 126 64 130 48 L139 50 C135 66 131 80 128 90 Z"/>
                  <path class="scoot-line" d="M134 49 L141 30"/>
                  <path class="scoot-bar" d="M131 29 H151"/>
                  <circle class="win-on" cx="143" cy="40" r="4"/>
                  <path class="scoot-body" d="M122 92 C124 80 152 80 154 92 L148 92 C146 86 130 86 128 92 Z"/>"""

SPEEDS = '<path class="speed" d="M-28 46 H-6"/><path class="speed sp2" d="M-42 64 H-10"/><path class="speed sp3" d="M-26 82 H-4"/>'

# the rider on its own, facing right: the hero trip, the intro and the footer ride-by
RIDER_SVG = f"""<svg viewBox="-46 14 208 100" focusable="false">
            <g>{SPEEDS}</g>
            <g class="scoot">
                  {SCOOTER_PARTS}
            </g>
          </svg>"""

# the driver card's cover: the rider on a moving road
SCOOTER_SVG = f"""<svg viewBox="0 0 240 128" focusable="false">
              <path class="speed" d="M24 60 H44"/>
              <path class="speed sp2" d="M14 76 H40"/>
              <path class="speed sp3" d="M26 92 H46"/>
              <path class="road-dots moving" d="M-7 119 H247"/>
              <g transform="translate(46 8)">
                <g class="scoot">
                  {SCOOTER_PARTS}
                </g>
              </g>
            </svg>"""

from food_items import FOOD  # noqa: E402

FOOD_ITEMS = "".join(
    f'<div class="food" data-food="{name}"><svg viewBox="0 0 100 100" focusable="false">'
    f'{inner.replace("{PIN_W}", str(PIN_W)).replace("{PIN_H}", str(PIN_H))}</svg></div>'
    for name, inner in FOOD)
FOOT_SCOOTER = f'<div class="foot-scooter">{RIDER_SVG}</div>'

CHECK = '<span class="st-dot"><svg viewBox="0 0 12 12" focusable="false"><path d="M2.5 6.2 5 8.6 9.5 3.6"/></svg></span>'
STATUS = [("st1", "Order placed", "done"), ("st2", "Accepted by the shop", "done"),
          ("st3", "Being prepared", "done"), ("st4", "On the way", "now"), ("st5", "Delivered", "")]
STATUS_ITEMS = "\n            ".join(
    f'<li{f" class={chr(34)}{c}{chr(34)}" if c else ""}>{CHECK}<span data-i18n="{k}">{t}</span></li>'
    for k, t, c in STATUS)


# ---------------------------------------------------------------- photos, icons, QR
def data_uri(name, mime="image/webp"):
    return f"data:{mime};base64," + base64.b64encode((HERE / "assets" / name).read_bytes()).decode()


def image_size(name):
    from PIL import Image
    with Image.open(HERE / "assets" / name) as im:
        return im.size


BAG_W, BAG_H = image_size("bag.webp")
QR = json.loads((HERE / "assets" / "qr.json").read_text())
QR_SVG = (f'<svg viewBox="-2 -2 {QR["size"] + 4} {QR["size"] + 4}" role="img" aria-label="QR code: jeetaklb.com" '
          f'focusable="false"><path d="{QR["d"]}"/></svg>')


# ---------------------------------------------------------------- intro
def intro_html(every_visit, replay):
    """The intro overlay. The early script sets the language and turns the intro on before the page
    paints, so nothing flashes first; the intro stays off for reduced motion and deep links, and,
    on the live site, after the first view in a browser session."""
    seen = "" if every_visit else 'sessionStorage.getItem("jeetak-intro")||'
    early = ('<script>(function(){var d=document.documentElement;'
             'try{var l=localStorage.getItem("jeetak-lang");'
             'if(l!=="ar"&&l!=="en")l=(navigator.language||"").toLowerCase().indexOf("ar")===0?"ar":"en";'
             'd.lang=l;d.dir=l==="ar"?"rtl":"ltr"}catch(e){}'
             'try{if(location.hash||' + seen + 'matchMedia("(prefers-reduced-motion: reduce)").matches)return;'
             'd.classList.add("intro-on")}catch(e){}})();</script>')
    overlay = f"""<div class="intro" id="intro" aria-hidden="true">
  <svg class="logo logo--pine intro-logo" viewBox="0 0 {LOCKUP["w"]} {LOCKUP["h"]}" focusable="false"><use href="#jk-lockup"/></svg>
  <svg class="intro-road" height="10" focusable="false"><line x1="-20" y1="5" x2="4000" y2="5"/></svg>
  <div class="intro-train" id="introTrain">
    <div class="intro-wipe"></div>
    <div class="intro-rider">
          {RIDER_SVG}
    </div>
  </div>
</div>"""
    chip = '\n<button class="intro-replay" id="introReplay" type="button">Replay intro</button>' if replay else ""
    return early + "\n" + overlay + chip


# ---------------------------------------------------------------- coverage map
import mapdraw  # noqa: E402

MAPS = mapdraw.maps()
assert not MAPS["wide"]["info"]["missing"], MAPS["wide"]["info"]["missing"]
MAP_HTML = f'''<div class="map-card" id="mapCard">
        <div class="map-frame">{MAPS["wide"]["svg"]}{MAPS["compact"]["svg"]}</div>
      </div>'''

# ---------------------------------------------------------------- assemble
body = (HERE / "body.html").read_text()
for key, val in {
    "LOGO_SYMBOLS": LOGO_SYMBOLS, "PIN_D": PIN_D, "PIN_W": PIN_W, "PIN_H": PIN_H,
    "WM_W": WORDMARK["w"], "WM_H": WORDMARK["h"], "LOCK_W": LOCKUP["w"], "LOCK_H": LOCKUP["h"],
    "BADGE_SYMBOLS": badge_symbols(),
    "STORE_IOS": store("customer", "ios"), "STORE_ANDROID": store("customer", "android"),
    "STORE_VENDOR_IOS": store("vendor", "ios"), "STORE_VENDOR_ANDROID": store("vendor", "android"),
    "STORE_DRIVER_IOS": store("driver", "ios"), "STORE_DRIVER_ANDROID": store("driver", "android"),
    "RIDER_SVG": RIDER_SVG, "SHOP_SVG": shop_svg(), "SCOOTER_SVG": SCOOTER_SVG,
    "STATUS_ITEMS": STATUS_ITEMS, "COVERAGE": MAP_HTML, "FOOD_ITEMS": FOOD_ITEMS + FOOT_SCOOTER,
    "BAG_IMG": data_uri("bag.webp"), "BAG_W": BAG_W, "BAG_H": BAG_H,
    "ICON_CUSTOMER": data_uri("icon-customer.webp"), "ICON_PARTNER": data_uri("icon-partner.webp"),
    "ICON_DRIVER": data_uri("icon-driver.webp"), "QR_SVG": QR_SVG,
}.items():
    body = body.replace("{{" + key + "}}", str(val))
left = set(re.findall(r"\{\{\w+\}\}", body))
assert left == {"{{INTRO}}", "{{SITE}}"}, left

css = (HERE / "style.css").read_text()
js = (HERE / "script.js").read_text()
js = js.replace("  /*{{STORE_LINKS}}*/", STORE_LINKS_JS).replace("  /*{{T_BASE}}*/", T_BASE_JS)
assert "{{" not in js, re.findall(r"\{\{\w+\}\}", js)
font_links = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
              '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
              f'<link rel="stylesheet" href="{FONTS}">')

# the artifact preview: plays the intro on every load and has a Replay button
OUT.mkdir(exist_ok=True)
preview_body = (body.replace("{{INTRO}}", intro_html(every_visit=True, replay=True))
                .replace("{{SITE}}", "https://jeetaklb.com"))
artifact = ('<title>Jeetak Redesign</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            f"{font_links}\n<style>\n{css}</style>\n{preview_body}\n<script>\n{js}</script>\n")
(OUT / "revamp.html").write_text(artifact)

# the same page as a deployable file
desc = "Food, groceries and anything else from shops near you, delivered across 24 villages in the Upper Metn."
site_body = body.replace("{{INTRO}}", intro_html(every_visit=False, replay=False)).replace("{{SITE}}", "")
site = f"""<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Jeetak · Delivery across the Upper Metn</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#E23C0E">
<link rel="canonical" href="https://jeetaklb.com/">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Jeetak">
<meta property="og:url" content="https://jeetaklb.com/">
<meta property="og:title" content="Jeetak · شو ما بدّك.">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://jeetaklb.com/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{font_links}
<style>
{css}</style>
</head>
<body>
{site_body}
<script>
{js}</script>
</body>
</html>
"""
SITE = OUT / "revamp-site"
SITE.mkdir(exist_ok=True)
(SITE / "index.html").write_text(site)

print("map", MAPS["wide"]["info"]["label_cost"], MAPS["compact"]["info"]["label_cost"])
print("artifact", (OUT / "revamp.html").stat().st_size, "bytes")
print("site", (SITE / "index.html").stat().st_size, "bytes")
