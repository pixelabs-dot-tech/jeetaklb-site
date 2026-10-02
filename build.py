"""Assemble the Jeetak landing page: an artifact preview and a deployable site."""
import json
import re
import shutil
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "out"
SITE = OUT / "site"

L = json.loads((ROOT / "logo_paths.json").read_text())
WORD_D, SLOGAN_D, PIN_D = L["wordmark"]["d"], L["slogan"]["d"], L["pin"]["d"]
WM_W, WM_H = L["wordmark"]["box"][2], L["wordmark"]["box"][3]
LOCK_W, LOCK_H = L["lockup_box"]
PIN_W, PIN_H = L["pin"]["box"][2], L["pin"]["box"][3]
PIN_CX, PIN_CY, PIN_R = 90.5, 90.2, 44

FONTS = ("https://fonts.googleapis.com/css2?family=Baloo+Bhaijaan+2:wght@600;800"
         "&family=Kanit:ital,wght@1,600;1,700&family=Readex+Pro:wght@400;500;600&display=swap")

# ---------------------------------------------------------------- landscape
FAR = ("M0 236 C110 214 200 196 310 204 C420 212 470 244 580 236 C690 228 760 182 870 178 "
       "C980 174 1040 222 1140 222 C1240 222 1300 176 1410 182 C1500 187 1560 214 1600 210 L1600 520 L0 520 Z")
MID = ("M0 300 C120 282 220 300 330 290 C450 279 500 262 610 268 C720 274 780 314 900 310 "
       "C1010 306 1080 266 1190 262 C1300 258 1380 296 1480 300 C1530 302 1570 296 1600 292 L1600 520 L0 520 Z")
NEAR = ("M0 412 C160 404 300 420 430 410 C560 398 650 362 760 342 C840 330 930 326 1000 334 "
        "C1100 346 1250 384 1400 398 C1480 406 1560 404 1600 402 L1600 520 L0 520 Z")
FORE = ("M0 488 C180 478 360 484 520 492 C700 501 900 480 1100 482 C1300 484 1460 492 1600 486 "
        "L1600 520 L0 520 Z")


def cubic_points(d):
    toks = re.findall(r"[MCLZ]|-?\d*\.?\d+", d)
    pts, cur, i = [], None, 0
    while i < len(toks):
        t = toks[i]
        if t == "M":
            cur = (float(toks[i + 1]), float(toks[i + 2])); i += 3
        elif t == "C":
            i += 1
            while i < len(toks) and toks[i] not in "MCLZ":
                p1 = (float(toks[i]), float(toks[i + 1]))
                p2 = (float(toks[i + 2]), float(toks[i + 3]))
                p3 = (float(toks[i + 4]), float(toks[i + 5]))
                for k in range(241):
                    s = k / 240; m = 1 - s
                    pts.append((m**3 * cur[0] + 3 * m * m * s * p1[0] + 3 * m * s * s * p2[0] + s**3 * p3[0],
                                m**3 * cur[1] + 3 * m * m * s * p1[1] + 3 * m * s * s * p2[1] + s**3 * p3[1]))
                cur = p3; i += 6
        else:
            break  # the closing L/Z box is not part of the ridge line
    return pts


EDGES = {name: cubic_points(d) for name, d in (("far", FAR), ("mid", MID), ("near", NEAR), ("fore", FORE))}


def edge(name, x):
    near = [p for p in EDGES[name] if abs(p[0] - x) < 3]
    return min(p[1] for p in near)


def trees(ridge, xs, scale, sink, cls):
    uses = []
    for i, x in enumerate(xs):
        s = scale * (1 + 0.09 * ((i % 3) - 1))
        uses.append(f'<use href="#tree" transform="translate({x} {edge(ridge, x) + sink:.1f}) scale({s:.2f})"/>')
    return f'<g class="{cls}">{"".join(uses)}</g>'


def huts(ridge, centers, offsets, scale, cls):
    uses = []
    for c in centers:
        for j, o in enumerate(offsets):
            x = c + o
            y = edge(ridge, x) + 1.5 + (2 if j % 2 else 0)
            uses.append(f'<use href="#hut" transform="translate({x} {y:.1f}) scale({scale})"/>')
    return f'<g class="{cls}">{"".join(uses)}</g>'


SHOP_X, HOUSE_X = 640, 960
SB = round(edge("fore", SHOP_X) + 1, 1)
HB = round(edge("near", HOUSE_X) + 1, 1)
END_X, END_Y = 916, round(edge("near", 916) + 3, 1)
ROUTE = (f"M{SHOP_X} {SB} C690 {SB - 3} 770 486 812 472 C858 457 872 444 842 432 "
         f"C806 418 742 414 752 396 C762 380 846 380 896 370 C922 362 924 344 {END_X} {END_Y}")
for x, y in ((812, 472), (842, 432), (752, 396), (896, 370)):
    assert y > edge("near", x) + 10, (x, y, edge("near", x))

HERO_SVG = f"""<svg id="heroArt" viewBox="0 0 1600 520" preserveAspectRatio="xMidYMax slice" aria-hidden="true" focusable="false">
      <defs>
        <radialGradient id="haze" cx="50%" cy="60%" r="62%">
          <stop offset="0" class="haze-in"/><stop offset="1" class="haze-out"/>
        </radialGradient>
        <g id="tree">
          <path class="tree-trunk" d="M0 0 C1 -8 -1 -16 2 -24"/>
          <path class="tree-top" d="M-30 -24 C-34 -32 -22 -40 -12 -37 C-8 -46 6 -48 13 -41 C22 -45 34 -38 31 -30 C36 -27 33 -21 26 -21 C8 -18 -14 -18 -30 -24 Z"/>
        </g>
        <g id="hut">
          <rect class="c-stone" x="-8" y="-11" width="16" height="11"/>
          <path class="c-roof" d="M-10 -11 L0 -18 L10 -11 Z"/>
          <rect class="win-on" x="-2.2" y="-7" width="4.4" height="4.4"/>
        </g>
        <mask id="trailMask" maskUnits="userSpaceOnUse" x="0" y="0" width="1600" height="520">
          <path id="trailReveal" d="{ROUTE}" fill="none" stroke="#fff" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>
        </mask>
      </defs>
      <rect width="1600" height="520" fill="url(#haze)"/>
      <path class="ridge-far" d="{FAR}"/>
      {huts("far", [380, 870, 1400], [-15, 0, 15], 0.55, "huts-far")}
      {trees("far", [60, 95, 150, 255, 290, 520, 555, 690, 730, 1000, 1040, 1250, 1290, 1520, 1560], 0.45, 2, "tree-far")}
      <path class="ridge-mid" d="{MID}"/>
      {huts("mid", [230, 640, 1200], [-24, -8, 8, 24], 0.8, "huts-mid")}
      {trees("mid", [40, 80, 120, 380, 415, 450, 500, 760, 800, 840, 1010, 1050, 1330, 1370, 1410, 1560], 0.7, 3, "tree-mid")}
      <path class="ridge-near" d="{NEAR}"/>
      {trees("near", [120, 170, 330, 380, 440, 520, 1060, 1110, 1170, 1250, 1320, 1470, 1520], 1.0, 5, "tree-near")}
      <path class="ridge-fore" d="{FORE}"/>
      <path id="route" class="road" d="{ROUTE}"/>
      <path class="trail trail-faint" d="{ROUTE}"/>
      <path id="trailBright" class="trail" d="{ROUTE}" mask="url(#trailMask)"/>
      {trees("fore", [90, 210, 560, 1400, 1510], 1.35, 7, "tree-fore")}
      <g transform="translate({SHOP_X} {SB})">
        <rect class="c-stone" x="-26" y="-30" width="52" height="30"/>
        <rect class="win-on" x="-21" y="-16" width="10" height="8"/>
        <rect class="win-on" x="11" y="-16" width="10" height="8"/>
        <rect class="c-door" x="-6" y="-15" width="12" height="15"/>
        <path class="c-roof" d="M-30 -30 H30 L26 -20 H-26 Z"/>
        <path class="awning-stripes" d="M-18 -30 L-19.5 -20 M-6 -30 L-6.5 -20 M6 -30 L6.5 -20 M18 -30 L19.5 -20"/>
      </g>
      <g id="destHouse" class="lit" transform="translate({HOUSE_X} {HB})">
        <rect class="c-stone" x="-30" y="-32" width="60" height="32"/>
        <path class="c-roof" d="M-37 -32 L0 -56 L37 -32 Z"/>
        <path class="win" d="M-19 -6 V-17 A4 4 0 0 1 -11 -17 V-6 Z M-4 -6 V-19 A4 4 0 0 1 4 -19 V-6 Z M11 -6 V-17 A4 4 0 0 1 19 -17 V-6 Z"/>
      </g>
      <g id="deliveredBadge" class="show" transform="translate({HOUSE_X} {HB - 78})">
        <g class="badge-in"><circle class="badge-disc" r="16"/><path class="badge-check" d="M-7 0.5 L-2 5.5 L7.5 -5"/></g>
      </g>
      <g id="movingPin" transform="translate({END_X} {END_Y})">
        <g class="pin-anim">
          <g transform="translate({-PIN_W / 2 * 0.22:.1f} {-PIN_H * 0.22:.1f}) scale(0.22)">
            <circle class="pin-core" cx="{PIN_CX}" cy="{PIN_CY}" r="{PIN_R}"/>
            <use href="#jk-pin" class="pin-fill"/>
          </g>
        </g>
      </g>
    </svg>"""

# ---------------------------------------------------------------- pieces
PHONE = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
         '<rect x="6" y="2.5" width="12" height="19" rx="2.6" fill="none" stroke="currentColor" stroke-width="1.8"/>'
         '<path d="M10.5 18.3h3" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>')


def store(app, key, name):
    return (f'<a class="store is-soon" data-app="{app}" data-store="{key}" aria-disabled="true">{PHONE}'
            f'<span><small>Coming soon on</small><strong>{name}</strong></span></a>')


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
    return f"""<svg viewBox="0 0 240 140" focusable="false">
              <path class="road-dots" d="M6 131 H234"/>
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
            </svg>"""


SCOOTER_SVG = f"""<svg viewBox="0 0 240 140" focusable="false">
              <path class="speed" d="M24 66 H44"/>
              <path class="speed sp2" d="M14 82 H40"/>
              <path class="speed sp3" d="M26 98 H46"/>
              <path class="road-dots moving" d="M-7 129 H247"/>
              <g transform="translate(46 18)">
                <g class="scoot">
                  <circle class="tire" cx="40" cy="96" r="15"/>
                  <g class="spokes"><path class="spoke" d="M31 96 H49 M35.5 88.2 L44.5 103.8 M35.5 103.8 L44.5 88.2"/></g>
                  <circle class="c-stone" cx="40" cy="96" r="5"/>
                  <circle class="tire" cx="138" cy="96" r="15"/>
                  <g class="spokes"><path class="spoke" d="M129 96 H147 M133.5 88.2 L142.5 103.8 M133.5 103.8 L142.5 88.2"/></g>
                  <circle class="c-stone" cx="138" cy="96" r="5"/>
                  <path class="rack" d="M10 60 H46"/>
                  <rect class="c-bag" x="8" y="22" width="38" height="36" rx="5"/>
                  <path class="bag-seam" d="M8 34 H46"/>
                  <svg x="19" y="36" width="16" height="20.4" viewBox="0 0 {PIN_W} {PIN_H}"><use href="#jk-pin" class="c-cream"/></svg>
                  <path class="scoot-body" d="M14 88 C12 74 22 62 38 60 H82 C88 60 92 64 92 70 V88 H62 C60 78 52 72 40 72 C28 72 20 78 18 88 Z"/>
                  <path class="scoot-dark" d="M42 60 C42 54 46 51 52 51 H80 C86 51 88 55 88 60 Z"/>
                  <path class="scoot-body" d="M90 82 H122 C124 82 125 84 125 86 V90 H90 Z"/>
                  <path class="scoot-body" d="M118 90 C122 78 126 64 130 48 L139 50 C135 66 131 80 128 90 Z"/>
                  <path class="scoot-line" d="M134 49 L141 30"/>
                  <path class="scoot-bar" d="M131 29 H151"/>
                  <circle class="win-on" cx="143" cy="40" r="4"/>
                  <path class="scoot-body" d="M122 92 C124 80 152 80 154 92 L148 92 C146 86 130 86 128 92 Z"/>
                </g>
              </g>
            </svg>"""


CHECK = '<span class="st-dot"><svg viewBox="0 0 12 12" focusable="false"><path d="M2.5 6.2 5 8.6 9.5 3.6"/></svg></span>'
STATUS = [("st1", "Order placed", "done"), ("st2", "Accepted by the shop", "done"),
          ("st3", "Being prepared", "done"), ("st4", "On the way", "now"), ("st5", "Delivered", "")]
STATUS_ITEMS = "\n          ".join(
    f'<li{f" class={chr(34)}{c}{chr(34)}" if c else ""}>{CHECK}<span data-i18n="{k}">{t}</span></li>'
    for k, t, c in STATUS)

VILLAGES = [
    ("Arsoun", "أرصون"), ("Bhamdoun", "بحمدون"), ("Btebyat", "بتبيات"), ("Btekhnay", "بتخنيه"),
    ("Bzebdine", "بزبدين"), ("Chbaniyeh", "الشبانية"), ("Deir El Harf", "دير الحرف"), ("Dlaibeh", "دليبة"),
    ("Falougha · Khalwet", "فالوغا · خلوات"), ("Hammana", "حمّانا"), ("Jouar El Houz", "جوار الحوز"),
    ("Khraybeh", "الخريبة"), ("Kornayel", "قرنايل"), ("Qalaa", "القلعة"), ("Qortada", "قرطاضة"),
    ("Qoubbei", "قبيع"), ("Qraiyeh", "القريّة"), ("Qseibe", "القصيبة"), ("Ras El Maten", "رأس المتن"),
    ("Salima", "صليما"), ("Saoufar", "صوفر"),
]
assert len(VILLAGES) == 21
SIGNS = "\n        ".join(
    f'<li class="sign" data-lat="{lat}" data-ar="{ar}"><span class="sign-ar" lang="ar">{ar}</span>'
    f'<span class="sign-lat">{lat}</span></li>' for lat, ar in VILLAGES)

body = (SRC / "body.html").read_text()
for key, val in {
    "WORDMARK_D": WORD_D, "SLOGAN_D": SLOGAN_D, "PIN_D": PIN_D,
    "WM_W": WM_W, "WM_H": WM_H, "LOCK_W": LOCK_W, "LOCK_H": LOCK_H, "PIN_W": PIN_W, "PIN_H": PIN_H,
    "STORE_IOS": store("customer", "ios", "App Store"), "STORE_ANDROID": store("customer", "android", "Google Play"),
    "STORE_VENDOR_IOS": store("vendor", "ios", "App Store"), "STORE_VENDOR_ANDROID": store("vendor", "android", "Google Play"),
    "STORE_DRIVER_IOS": store("driver", "ios", "App Store"), "STORE_DRIVER_ANDROID": store("driver", "android", "Google Play"),
    "SHOP_SVG": shop_svg(), "SCOOTER_SVG": SCOOTER_SVG,
    "HERO_SVG": HERO_SVG, "STATUS_ITEMS": STATUS_ITEMS, "SIGNS": SIGNS,
}.items():
    body = body.replace("{{" + key + "}}", str(val))
assert "{{" not in body, re.findall(r"\{\{\w+\}\}", body)

css = (SRC / "style.css").read_text()
js = (SRC / "script.js").read_text()
font_links = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
              '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
              f'<link rel="stylesheet" href="{FONTS}">')

# ---------------------------------------------------------------- artifact preview
OUT.mkdir(exist_ok=True)
artifact = f"<title>jeetaklb.com</title>\n{font_links}\n<style>\n{css}</style>\n{body}\n<script>\n{js}</script>\n"
(OUT / "jeetaklb.html").write_text(artifact)

# ---------------------------------------------------------------- deployable site
fav = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#E23C0E"/>'
       f'<g transform="translate(14.8 10) scale(0.19)"><path fill="#fff" fill-rule="evenodd" d="{PIN_D}"/></g></svg>')
fav_uri = "data:image/svg+xml," + urllib.parse.quote(fav)
desc = "Food, groceries and anything else from shops near you, delivered across 21 villages in the Upper Metn."
site = f"""<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Jeetak · Delivery across the Upper Metn</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#1D3D2F">
<link rel="canonical" href="https://jeetaklb.com/">
<link rel="icon" type="image/svg+xml" href="{fav_uri}">
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
{body}
<script>
{js}</script>
</body>
</html>
"""
SITE.mkdir(exist_ok=True)
(SITE / "index.html").write_text(site)

# ---------------------------------------------------------------- link preview image
og_html = f"""<html><body style="margin:0;width:1200px;height:630px;background:#E23C0E;display:grid;place-items:center">
<svg viewBox="0 0 {LOCK_W} {LOCK_H}" width="640" fill="#fff"><path fill-rule="evenodd" d="{WORD_D}"/><path fill-rule="evenodd" d="{SLOGAN_D}"/></svg>
</body></html>"""
from playwright.sync_api import sync_playwright  # noqa: E402
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 630})
    page.set_content(og_html)
    page.screenshot(path=str(SITE / "og-image.png"))
    browser.close()

print("shop base", SB, "house base", HB, "route end", END_X, END_Y)
print("artifact", (OUT / "jeetaklb.html").stat().st_size, "bytes")
print("site", (SITE / "index.html").stat().st_size, "bytes;", "og", (SITE / "og-image.png").stat().st_size, "bytes")
