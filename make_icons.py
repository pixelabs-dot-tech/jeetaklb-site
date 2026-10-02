"""Turn the app icon artwork into the site's favicon and home-screen icons."""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
SRC = ROOT / "icon-source.jpg"
OUT = ROOT / "out" / "site"


def find_tile(a):
    """Bounding box, corner radius and flat colour of the orange tile."""
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    orange = (r > 200) & (g > 50) & (g < 140) & (b < 90)
    ys, xs = np.where(orange)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    t = 0
    while not orange[y0 + t, x0 + t]:
        t += 1
    radius = t / (1 - 2 ** -0.5)
    colour = tuple(int(v) for v in np.median(a[orange], axis=0))
    return (x0, y0, x1, y1), radius, colour


def rounded_mask(size, radius, inset=0, scale=4):
    big = Image.new("L", (size * scale, size * scale), 0)
    ImageDraw.Draw(big).rounded_rectangle(
        (inset * scale, inset * scale, (size - inset) * scale - 1, (size - inset) * scale - 1),
        radius=max(radius - inset, 0) * scale, fill=255)
    return big.resize((size, size), Image.LANCZOS)


def build():
    src = Image.open(SRC).convert("RGB")
    (x0, y0, x1, y1), radius, colour = find_tile(np.array(src).astype(int))
    side = max(x1 - x0, y1 - y0) + 1
    tile = src.crop((x0, y0, x0 + side, y0 + side))

    # Full square: the tile's own pixels inside its rounded outline, flat orange
    # outside it, so the grey background and anti-aliased edge are gone.
    full = Image.new("RGB", (side, side), colour)
    full.paste(tile, (0, 0), rounded_mask(side, radius, inset=3))

    # Rounded tile with transparent corners, for browser tabs.
    rounded = full.convert("RGBA")
    rounded.putalpha(rounded_mask(side, radius))

    OUT.mkdir(parents=True, exist_ok=True)
    full.resize((180, 180), Image.LANCZOS).save(OUT / "apple-touch-icon.png", optimize=True)
    rounded.resize((192, 192), Image.LANCZOS).save(OUT / "icon-192.png", optimize=True)
    rounded.resize((32, 32), Image.LANCZOS).save(OUT / "favicon-32.png", optimize=True)
    rounded.resize((256, 256), Image.LANCZOS).save(
        OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    return side, radius, colour


if __name__ == "__main__":
    side, radius, colour = build()
    print("tile", side, "px, corner radius", round(radius, 1), "colour #%02X%02X%02X" % colour)
    for f in ("favicon.ico", "favicon-32.png", "icon-192.png", "apple-touch-icon.png"):
        print(f, (OUT / f).stat().st_size, "bytes")
