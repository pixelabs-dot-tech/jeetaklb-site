"""Measure the map's village labels in the page fonts (Cairo) -> revamp/label_widths.json.

The widths feed village_map.py, which places the labels so they don't overlap.
Needs the fonts on disk: npm i @fontsource/cairo, then JEETAK_FONTS=<...>/node_modules/@fontsource
"""
import json
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent.parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import village_map  # noqa: E402

FONTS = Path(os.environ["JEETAK_FONTS"]) / "cairo" / "files"
EN = "600 15px Cairo"      # .map-label
AR = "700 16px Cairo"      # .map-ar .map-label
villages = village_map.load_villages()

faces = "".join(
    f'@font-face{{font-family:Cairo;font-weight:{w};src:url({(FONTS / f"cairo-{sub}-{w}-normal.woff2").as_uri()}) format("woff2");'
    f'unicode-range:{rng}}}'
    for w in (600, 700)
    for sub, rng in (("latin", "U+0000-00FF,U+2000-206F"), ("arabic", "U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFC")))
texts = "".join(f'<text class="en" y="20">{lat}</text><text class="ar" lang="ar" y="60">{ar}</text>' for lat, ar in villages)
html = f'<style>{faces} .en{{font:{EN}}} .ar{{font:{AR}}}</style><svg width="900" height="100">{texts}</svg>'

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto((HERE / "tools" / "measure_labels.py").as_uri())   # a file:// origin, so the fonts may load
    pg.set_content(html)
    pg.evaluate(f"() => Promise.all([document.fonts.load('{EN}', 'Hamana'), document.fonts.load('{AR}', 'حمّانا')])")
    ok = pg.evaluate(f"() => [document.fonts.check('{EN}', 'Hammana'), document.fonts.check('{AR}', 'حمّانا')]")
    en = pg.evaluate("() => [...document.querySelectorAll('.en')].map(t => t.getComputedTextLength())")
    ar = pg.evaluate("() => [...document.querySelectorAll('.ar')].map(t => t.getComputedTextLength())")
    b.close()
assert all(ok), ok
out = {lat: [en[i], ar[i]] for i, (lat, _) in enumerate(villages)}
(HERE / "label_widths.json").write_text(json.dumps(out, ensure_ascii=False, indent=0))
old = village_map.WIDTHS
for lat, _ in villages:
    print(f"{lat:16s} en {old[lat][0]:6.1f} -> {out[lat][0]:6.1f}   ar {old[lat][1]:6.1f} -> {out[lat][1]:6.1f}")
