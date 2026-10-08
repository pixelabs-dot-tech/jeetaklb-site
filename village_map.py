"""Build the coverage map: an SVG of the Upper Metn with every village Jeetak delivers to.

Positions come from village_coords.py (GeoNames). Labels are placed so they don't
overlap, using label widths measured in the page fonts (label_widths.json).
The terrain contour lines are decorative: they rise from west to east like the
real slopes, but they are not survey data.
"""
import json
import math
import random
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from village_coords import COORDS

ROOT = Path(__file__).parent
WIDTHS = json.loads((ROOT / "label_widths.json").read_text())

W = 1000.0                      # viewBox width
MARGIN_KM = (2.0, 1.9, 2.0, 2.0)  # left, top, right, bottom
DOT_R = 5.5
FONT_EN, FONT_AR = 15.0, 16.0
LABEL_H_EN, LABEL_H_AR = 19.0, 22.0
GAP = 7.0
ZONE_SIGMA_KM, ZONE_LEVEL = 1.05, 0.45   # delivery-area blob: spread around each village, outline level
BEIRUT_Y, BEKAA_Y = 0.5, 0.62            # edge arrows, as fractions of the map height


def project():
    lats = [c[0] for c in COORDS.values()]
    lons = [c[1] for c in COORDS.values()]
    lat0 = (min(lats) + max(lats)) / 2
    kx = 111.32 * math.cos(math.radians(lat0))   # km per degree of longitude
    ky = 110.57                                  # km per degree of latitude
    span_x = (max(lons) - min(lons)) * kx + MARGIN_KM[0] + MARGIN_KM[2]
    s = W / span_x                               # viewBox units per km
    span_y = (max(lats) - min(lats)) * ky + MARGIN_KM[1] + MARGIN_KM[3]
    h = round(span_y * s)
    pts = {}
    for name, (lat, lon) in COORDS.items():
        x = ((lon - min(lons)) * kx + MARGIN_KM[0]) * s
        y = ((max(lats) - lat) * ky + MARGIN_KM[1]) * s
        pts[name] = (x, y)
    return pts, s, float(h)


# ------------------------------------------------------------------ terrain and zone
def smooth_noise(xx, yy, seed, scale):
    rng = np.random.default_rng(seed)
    z = np.zeros_like(xx)
    for _ in range(14):
        fx, fy = rng.uniform(0.4, 1.6, 2) / scale
        ph = rng.uniform(0, 2 * math.pi, 2)
        amp = rng.uniform(0.5, 1.0)
        z += amp * np.sin(xx * fx + ph[0]) * np.cos(yy * fy + ph[1])
    return z / 14


def contour_paths(field, xs, ys, levels):
    fig = plt.figure()
    cs = plt.contour(xs, ys, field, levels=levels)
    out = []
    for lvl, segs in zip(cs.levels, cs.allsegs):
        for seg in segs:
            if len(seg) < 6:
                continue
            out.append((lvl, rdp(seg, 0.6)))
    plt.close(fig)
    return out


def rdp(points, eps):  # Ramer-Douglas-Peucker simplification
    pts = np.asarray(points)
    if len(pts) < 3:
        return pts
    start, end = pts[0], pts[-1]
    line = end - start
    norm = np.hypot(*line)
    if norm == 0:
        d = np.hypot(*(pts - start).T)
    else:
        rel = pts - start
        d = np.abs(line[0] * rel[:, 1] - line[1] * rel[:, 0]) / norm
    i = int(np.argmax(d))
    if d[i] > eps:
        left = rdp(pts[: i + 1], eps)
        right = rdp(pts[i:], eps)
        return np.vstack([left[:-1], right])
    return np.vstack([start, end])


def path_d(pts, closed=False):
    p = [f"{pts[0][0]:.1f} {pts[0][1]:.1f}"] + [f"{x:.1f} {y:.1f}" for x, y in pts[1:]]
    return "M" + "L".join(p) + ("Z" if closed else "")


def terrain_and_zone(pts, s, h):
    nx, ny = 220, int(220 * h / W)
    xs = np.linspace(-10, W + 10, nx)
    ys = np.linspace(-10, h + 10, ny)
    xx, yy = np.meshgrid(xs, ys)
    km_x, km_y = xx / s, yy / s
    # Rises from about 650 m in the west to the high ridge in the east.
    elev = 760 + 38 * km_x + 520 * np.exp(-((km_x - 21) ** 2) / 10)
    elev += 330 * smooth_noise(km_x, km_y, 7, 2.3) + 120 * smooth_noise(km_x, km_y, 11, 0.9)
    for cx, cy, amp, rad in ((4.5, 3.0, 160, 1.6), (9.0, 9.5, -150, 2.2), (13.5, 2.5, 130, 1.4), (6.5, 10.5, 120, 1.5)):
        elev += amp * np.exp(-(((km_x - cx) ** 2 + (km_y - cy) ** 2) / (2 * rad ** 2)))
    levels = list(range(600, 2200, 80))
    contours = contour_paths(elev, xs, ys, levels)

    # Delivery zone: a soft blob around the villages.
    sigma = ZONE_SIGMA_KM * s
    field = np.zeros_like(xx)
    for x, y in pts.values():
        field += np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (2 * sigma ** 2))
    zone = contour_paths(field, xs, ys, [ZONE_LEVEL])
    return contours, [seg for _, seg in zone]


def zone_field(pts, s):
    """The same field the zone outline is traced from, for testing single points."""
    p = np.array(list(pts.values()))
    two_sigma2 = 2 * (ZONE_SIGMA_KM * s) ** 2

    def f(x, y):
        return float(np.exp(-((p[:, 0] - x) ** 2 + (p[:, 1] - y) ** 2) / two_sigma2).sum())
    return f


# ------------------------------------------------------------------ label placement
DIRS = {
    "E": (1, 0), "W": (-1, 0), "N": (0, -1), "S": (0, 1),
    "NE": (0.8, -0.8), "NW": (-0.8, -0.8), "SE": (0.8, 0.8), "SW": (-0.8, 0.8),
}
DIR_COST = {"E": 0.0, "W": 0.25, "N": 0.45, "S": 0.45, "NE": 0.6, "NW": 0.7, "SE": 0.6, "SW": 0.7}


def candidates(x, y, w, h):
    out = []
    for dist_i, (dist, extra) in enumerate([(0.0, 0.0), (26.0, 2.2), (48.0, 4.5)]):
        for key, (dx, dy) in DIRS.items():
            ox = x + dx * (DOT_R + GAP + dist)
            oy = y + dy * (DOT_R + GAP * 0.6 + dist)
            if dx > 0:
                left = ox
            elif dx < 0:
                left = ox - w
            else:
                left = ox - w / 2
            if dy > 0:
                top = oy
            elif dy < 0:
                top = oy - h
            else:
                top = oy - h / 2
            out.append({"box": (left, top, left + w, top + h), "leader": dist_i > 0,
                        "cost": DIR_COST[key] + extra})
    return out


def overlap(a, b, pad=3.0):
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    ix = min(ax1 + pad, bx1 + pad) - max(ax0 - pad, bx0 - pad)
    iy = min(ay1 + pad, by1 + pad) - max(ay0 - pad, by0 - pad)
    return max(0.0, ix) * max(0.0, iy)


def box_hits_circle(box, cx, cy, r):
    x0, y0, x1, y1 = box
    nx = min(max(cx, x0), x1)
    ny = min(max(cy, y0), y1)
    return (nx - cx) ** 2 + (ny - cy) ** 2 < (r + 2.5) ** 2


def leader_end(box, x, y):
    x0, y0, x1, y1 = box
    return (min(max(x, x0), x1), min(max(y, y0), y1))


def seg_hits_box(p, q, box):
    # sample along the segment; good enough for short leaders
    for t in np.linspace(0.15, 0.85, 8):
        sx = p[0] + (q[0] - p[0]) * t
        sy = p[1] + (q[1] - p[1]) * t
        if box[0] - 1 < sx < box[2] + 1 and box[1] - 1 < sy < box[3] + 1:
            return True
    return False


def place_labels(pts, widths, label_h, bounds, reserved, field=None, seed=3, steps=60000):
    names = list(pts)
    cands = {n: candidates(*pts[n], widths[n], label_h) for n in names}
    W_, H_ = bounds

    def unary(n, c):
        cost = c["cost"] * 6
        b = c["box"]
        if b[0] < 8 or b[1] < 8 or b[2] > W_ - 8 or b[3] > H_ - 8:
            cost += 400
        for r in reserved:
            cost += overlap(b, r, 2) * 2
        for m in names:
            if box_hits_circle(b, *pts[m], DOT_R):
                cost += 160
        if field is not None:
            # keep labels clear of the dotted delivery-area line: test the box edge (plus the halo)
            x0, y0, x1, y1 = b[0] - 4, b[1] - 4, b[2] + 4, b[3] + 4
            xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
            ring = ((x0, y0), (xm, y0), (x1, y0), (x1, ym), (x1, y1), (xm, y1), (x0, y1), (x0, ym))
            cost += 5 * sum(1 for sx, sy in ring if field(sx, sy) < ZONE_LEVEL)
        return cost

    for n in names:
        for c in cands[n]:
            c["u"] = unary(n, c)
            c["seg"] = (pts[n], leader_end(c["box"], *pts[n])) if c["leader"] else None

    def pair(a, ca, b, cb):
        cost = overlap(ca["box"], cb["box"]) * 3
        if ca["seg"] and seg_hits_box(*ca["seg"], cb["box"]):
            cost += 60
        if cb["seg"] and seg_hits_box(*cb["seg"], ca["box"]):
            cost += 60
        return cost

    rng = random.Random(seed)
    choice = {n: min(cands[n], key=lambda c: c["u"]) for n in names}

    def total():
        t = sum(choice[n]["u"] for n in names)
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                t += pair(a, choice[a], b, choice[b])
        return t

    cur = total()
    best, best_cost = dict(choice), cur
    temp = 60.0
    decay = (0.05 / temp) ** (1 / steps)
    for _ in range(steps):
        n = rng.choice(names)
        old = choice[n]
        new = rng.choice(cands[n])
        if new is old:
            continue
        delta = new["u"] - old["u"]
        for m in names:
            if m != n:
                delta += pair(n, new, m, choice[m]) - pair(n, old, m, choice[m])
        if delta <= 0 or rng.random() < math.exp(-delta / max(temp, 0.01)):
            choice[n] = new
            cur += delta
            if cur < best_cost - 1e-9:
                best, best_cost = dict(choice), cur
        temp *= decay
    return best, best_cost


# ------------------------------------------------------------------ SVG
def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;")


def build(villages):
    """villages: list of (latin name, arabic name). Returns (svg, info)."""
    ar_of = dict(villages)
    pts, s, h = project()
    names = [n for n, _ in villages if n in pts]
    missing = [n for n, _ in villages if n not in pts]

    contours, zone = terrain_and_zone(pts, s, h)

    # map furniture (reserved so labels avoid it)
    scale_km = 2
    sb_x, sb_y = 34.0, h - 40.0
    sb_w = scale_km * s
    by = h * BEIRUT_Y    # edge arrows: Beirut on the west side, the Bekaa on the east
    ky_ = h * BEKAA_Y
    reserved = [
        (sb_x - 6, sb_y - 26, sb_x + sb_w + 50, sb_y + 14),       # scale bar
        (W - 66, 18, W - 18, 84),                                  # north arrow
        (14, by - 22, 112, by + 22),                               # Beirut
        (W - 108, ky_ - 22, W - 14, ky_ + 22),                     # Bekaa
        (W - 230, h - 56, W - 18, h - 18),                          # legend
    ]
    # label_widths.json holds widths measured in the page fonts; a village that isn't in it
    # yet gets a generous estimate so its label still can't collide with its neighbours
    en_w = {n: WIDTHS[n][0] if n in WIDTHS else len(n) * 10.5 for n in names}
    ar_w = {n: WIDTHS[n][1] if n in WIDTHS else len(ar_of[n]) * 9.0 for n in names}
    field = zone_field({n: pts[n] for n in names}, s)
    en_place, en_cost = place_labels({n: pts[n] for n in names}, en_w, LABEL_H_EN, (W, h), reserved, field)
    ar_place, ar_cost = place_labels({n: pts[n] for n in names}, ar_w, LABEL_H_AR, (W, h), reserved, field, seed=5)

    # Hammana-outward order for the reveal ripple
    hx, hy = pts.get("Hammana", (W / 2, h / 2))
    order = sorted(names, key=lambda n: math.hypot(pts[n][0] - hx, pts[n][1] - hy))
    delay = {n: i * 70 for i, n in enumerate(order)}

    def label_svg(n, place, lang, font, lh):
        b = place["box"]
        x, y = pts[n]
        parts = []
        if place["leader"]:
            ex, ey = leader_end(b, x, y)
            parts.append(f'<path class="map-leader" d="M{x:.1f} {y:.1f}L{ex:.1f} {ey:.1f}"/>')
        text = n if lang == "en" else ar_of[n]
        base = b[1] + lh * (0.74 if lang == "en" else 0.72)
        parts.append(f'<text class="map-label" x="{b[0]:.1f}" y="{base:.1f}">{esc(text)}</text>')
        return "".join(parts)

    contour_svg = []
    for lvl, seg in contours:
        cls = "map-contour is-index" if lvl % 400 == 0 else "map-contour"
        contour_svg.append(f'<path class="{cls}" d="{path_d(seg)}"/>')

    zone_svg = "".join(f'<path class="map-zone" d="{path_d(seg, closed=True)}"/>' for seg in zone)
    zone_line = "".join(f'<path class="map-zone-line" d="{path_d(seg, closed=True)}"/>' for seg in zone)

    villages_svg = []
    for n in names:
        x, y = pts[n]
        villages_svg.append(
            f'<g class="map-v" style="--d:{delay[n]}ms">'
            f'<circle class="map-ring" cx="{x:.1f}" cy="{y:.1f}" r="{DOT_R}"/>'
            f'<circle class="map-dot" cx="{x:.1f}" cy="{y:.1f}" r="{DOT_R}"/>'
            f'<g class="map-en">{label_svg(n, en_place[n], "en", FONT_EN, LABEL_H_EN)}</g>'
            f'<g class="map-ar" lang="ar">{label_svg(n, ar_place[n], "ar", FONT_AR, LABEL_H_AR)}</g>'
            f'<circle class="map-hit" cx="{x:.1f}" cy="{y:.1f}" r="16"/>'
            f'</g>')

    ticks = "".join(
        f'<rect class="{"map-sb-a" if i % 2 == 0 else "map-sb-b"}" x="{sb_x + i * s:.1f}" y="{sb_y - 5:.1f}" width="{s:.1f}" height="6"/>'
        for i in range(scale_km))
    scale_svg = (f'<g class="map-scale">{ticks}'
                 f'<text class="map-small" x="{sb_x:.1f}" y="{sb_y - 12:.1f}">0</text>'
                 f'<text class="map-small map-en" x="{sb_x + sb_w + 8:.1f}" y="{sb_y + 1:.1f}">{scale_km} km</text>'
                 f'<text class="map-small map-ar" lang="ar" x="{sb_x + sb_w + 8:.1f}" y="{sb_y + 2:.1f}">{scale_km} كلم</text></g>')

    north = (f'<g class="map-north" transform="translate({W - 42:.1f} 30)">'
             f'<path class="map-north-a" d="M0 0 L9 26 L0 20 Z"/><path class="map-north-b" d="M0 0 L-9 26 L0 20 Z"/>'
             f'<text class="map-small map-n" x="0" y="44" text-anchor="middle">N</text></g>')

    edges = (f'<g class="map-edge">'
             f'<path class="map-arrow" d="M22 {by:.1f} h26 M22 {by:.1f} l9 -6 M22 {by:.1f} l9 6"/>'
             f'<text class="map-small map-en" x="56" y="{by + 4.5:.1f}">Beirut</text>'
             f'<text class="map-small map-ar" lang="ar" x="56" y="{by + 5:.1f}">بيروت</text>'
             f'<path class="map-arrow" d="M{W - 22:.1f} {ky_:.1f} h-26 M{W - 22:.1f} {ky_:.1f} l-9 -6 M{W - 22:.1f} {ky_:.1f} l-9 6"/>'
             f'<text class="map-small map-en" x="{W - 56:.1f}" y="{ky_ + 4.5:.1f}" text-anchor="end">Bekaa</text>'
             f'<text class="map-small map-ar" lang="ar" x="{W - 56:.1f}" y="{ky_ + 5:.1f}" text-anchor="end">البقاع</text>'
             f'</g>')

    lx, ly = W - 222, h - 37
    legend = (f'<g class="map-legend">'
              f'<path class="map-zone-line" d="M{lx:.1f} {ly:.1f} h34"/>'
              f'<text class="map-small map-en" x="{lx + 44:.1f}" y="{ly + 4.5:.1f}">Delivery area</text>'
              f'<text class="map-small map-ar" lang="ar" x="{lx + 44:.1f}" y="{ly + 5:.1f}">منطقة التوصيل</text>'
              f'</g>')

    names_list = ", ".join(n for n, _ in villages)
    svg = (f'<svg class="village-map" viewBox="0 0 {W:.0f} {h:.0f}" role="img" aria-labelledby="mapTitle" focusable="false">'
           f'<title id="mapTitle">Map of the villages Jeetak delivers to in the Upper Metn: {esc(names_list)}</title>'
           f'<rect class="map-bg" width="{W:.0f}" height="{h:.0f}" rx="0"/>'
           f'<g class="map-contours">{"".join(contour_svg)}</g>'
           f'{zone_svg}{zone_line}'
           f'{edges}{north}{scale_svg}{legend}'
           f'<g class="map-villages">{"".join(villages_svg)}</g>'
           f'<g class="map-drop" id="mapDrop" transform="translate(-100 -100)"><g class="map-drop-pin">'
           f'<svg x="-9" y="-23" width="18" height="23" viewBox="0 0 181 231" overflow="visible">'
           f'<circle class="pin-core" cx="90.5" cy="90.2" r="44"/><use href="#jk-pin" class="pin-fill"/></svg></g></g>'
           f'</svg>')
    info = {"width": W, "height": h, "hammana_x": hx / W, "missing": missing,
            "label_cost": [round(en_cost, 1), round(ar_cost, 1)], "km": s}
    return svg, info


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(ROOT))
    src = (ROOT / "build.py").read_text()
    a = src.index("VILLAGES = [")
    b = src.index("]", src.index('("Saoufar", "صوفر")')) + 1
    ns = {}
    exec(src[a:b], ns)
    svg, info = build(ns["VILLAGES"])
    (ROOT / "out" / "map.svg").write_text(svg)
    print(info, len(svg), "bytes")
