"""Build the coverage map: an SVG of the Upper Metn with every village Jeetak delivers to.

Two layouts are drawn from the same data:
- "wide" for laptops and tablets (1000 units across, about 1:1 on a desktop screen)
- "compact" for phones (350 units across, about 1:1 on a phone), with its own label
  layout so every name stays readable without zooming or swiping.

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
WIDTHS = json.loads((ROOT / "label_widths.json").read_text())   # measured at FONT_EN / FONT_AR

W = 1000.0                      # wide viewBox width
MARGIN_KM = (2.0, 1.9, 2.0, 2.0)  # left, top, right, bottom
DOT_R = 5.5
FONT_EN, FONT_AR = 15.0, 16.0
LABEL_H_EN, LABEL_H_AR = 19.0, 22.0
GAP = 7.0
ZONE_SIGMA_KM, ZONE_LEVEL = 1.05, 0.45   # delivery-area blob: spread around each village, outline level
BEIRUT_Y, BEKAA_Y = 0.5, 0.62            # edge arrows, as fractions of the map height

LAYOUTS = {
    "wide": {
        "W": W, "margin_km": MARGIN_KM, "dot_r": DOT_R, "font": (FONT_EN, FONT_AR),
        "label_h": (LABEL_H_EN, LABEL_H_AR), "gap": GAP, "grid": 220, "pad": 10,
        "levels": (600, 2200, 80), "index": (400, 0), "rdp": 0.6,
    },
    "compact": {
        "W": 350.0, "margin_km": (1.45, 1.5, 1.45, 1.75), "dot_r": 3.6, "font": (10.5, 12.0),
        "label_h": (13.5, 16.5), "gap": 3.5, "grid": 175, "pad": 4,
        # Phones are tall and the area is wide: north-south distances are drawn 1.3x longer
        # so the labels around Hammana have room. (No scale bar on this one for that reason.)
        "stretch": 1.3,
        "levels": (600, 2200, 240), "index": (960, 600), "rdp": 0.3,
        # label search: distances from the dot (leader lines from leader_min on)
        "dists": (0.0, 7.0, 14.0, 22.0, 31.0, 41.0, 52.0), "leader_min": 7.0, "dist_cost": (0.35, 6.0),
        # labels side by side need a wider gap than labels stacked, or two names read as one
        "zone_w": 0.8, "overlap_pad": (5.0, 1.5), "steps": 300000, "seeds": (3, 11, 29, 47),
        "edge_y": (0.6, 0.62),     # Beirut and Bekaa arrows, as fractions of the map height
    },
}


def project(L=LAYOUTS["wide"]):
    Wl, margin = L["W"], L["margin_km"]
    lats = [c[0] for c in COORDS.values()]
    lons = [c[1] for c in COORDS.values()]
    lat0 = (min(lats) + max(lats)) / 2
    kx = 111.32 * math.cos(math.radians(lat0))   # km per degree of longitude
    ky = 110.57 * L.get("stretch", 1.0)          # km per degree of latitude (the phone map is drawn taller)
    span_x = (max(lons) - min(lons)) * kx + margin[0] + margin[2]
    s = Wl / span_x                              # viewBox units per km
    span_y = (max(lats) - min(lats)) * ky + margin[1] + margin[3]
    h = round(span_y * s)
    pts = {}
    for name, (lat, lon) in COORDS.items():
        x = ((lon - min(lons)) * kx + margin[0]) * s
        y = ((max(lats) - lat) * ky + margin[1]) * s
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


def contour_paths(field, xs, ys, levels, eps=0.6):
    fig = plt.figure()
    cs = plt.contour(xs, ys, field, levels=levels)
    out = []
    for lvl, segs in zip(cs.levels, cs.allsegs):
        for seg in segs:
            if len(seg) < 6:
                continue
            out.append((lvl, rdp(seg, eps)))
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


def terrain_and_zone(pts, s, h, L=LAYOUTS["wide"]):
    Wl, pad = L["W"], L["pad"]
    nx, ny = L["grid"], int(L["grid"] * h / Wl)
    xs = np.linspace(-pad, Wl + pad, nx)
    ys = np.linspace(-pad, h + pad, ny)
    xx, yy = np.meshgrid(xs, ys)
    # the terrain is defined in the wide map's km grid, so both layouts show the same hills
    km_x = xx / s + (MARGIN_KM[0] - L["margin_km"][0])
    st = L.get("stretch", 1.0)
    if st == 1.0:
        km_y = yy / s + (MARGIN_KM[1] - L["margin_km"][1])
    else:
        km_y = (yy / s - L["margin_km"][1]) / st + MARGIN_KM[1]
    # Rises from about 650 m in the west to the high ridge in the east.
    elev = 760 + 38 * km_x + 520 * np.exp(-((km_x - 21) ** 2) / 10)
    elev += 330 * smooth_noise(km_x, km_y, 7, 2.3) + 120 * smooth_noise(km_x, km_y, 11, 0.9)
    for cx, cy, amp, rad in ((4.5, 3.0, 160, 1.6), (9.0, 9.5, -150, 2.2), (13.5, 2.5, 130, 1.4), (6.5, 10.5, 120, 1.5)):
        elev += amp * np.exp(-(((km_x - cx) ** 2 + (km_y - cy) ** 2) / (2 * rad ** 2)))
    levels = list(range(*L["levels"]))
    contours = contour_paths(elev, xs, ys, levels, L["rdp"])

    # Delivery zone: a soft blob around the villages.
    sigma = ZONE_SIGMA_KM * s
    field = np.zeros_like(xx)
    for x, y in pts.values():
        field += np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (2 * sigma ** 2))
    zone = contour_paths(field, xs, ys, [ZONE_LEVEL], L["rdp"])
    return contours, [seg for _, seg in zone]


def zone_field(pts, s):
    """The same field the zone outline is traced from, for testing single points."""
    p = np.array(list(pts.values()))
    two_sigma2 = 2 * (ZONE_SIGMA_KM * s) ** 2

    def f(x, y):
        return float(np.exp(-((p[:, 0] - x) ** 2 + (p[:, 1] - y) ** 2) / two_sigma2).sum())
    return f


# ------------------------------------------------------------------ label placement (wide)
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


# ------------------------------------------------------------------ label placement (compact)
# 16 directions, clockwise from east (y points down), with a preference cost:
# right of the dot reads best, then left, then above/below, then the diagonals.
DIR16 = ((0, 0.0), (22.5, 0.3), (45, 0.6), (67.5, 0.55), (90, 0.45), (112.5, 0.6), (135, 0.7), (157.5, 0.45),
         (180, 0.25), (202.5, 0.45), (225, 0.7), (247.5, 0.6), (270, 0.45), (292.5, 0.55), (315, 0.6), (337.5, 0.3))


def fan_candidates(x, y, w, h, L):
    r, gap = L["dot_r"], L["gap"]
    out = []
    lin, quad = L["dist_cost"]   # long leaders get expensive fast
    for d in L["dists"]:
        for ang, pref in DIR16:
            c, sn = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            px = x + c * (r + gap + d)
            py = y + sn * (r + gap * 0.6 + d)
            # how much of the label sits left of / above the anchor; labels straight above, below
            # or beside a dot may also slide along it, which helps in tight clusters
            fxs = (0.0,) if c > 0.38 else ((1.0,) if c < -0.38 else (0.5, 0.2, 0.8))
            fys = (0.0,) if sn > 0.38 else ((1.0,) if sn < -0.38 else (0.5, 0.15, 0.85))
            for fx in fxs:
                for fy in fys:
                    left, top = px - w * fx, py - h * fy
                    box = (left, top, left + w, top + h)
                    seg = None
                    if d >= L["leader_min"]:
                        ex, ey = leader_end(box, x, y)
                        ln = math.hypot(ex - x, ey - y) or 1.0
                        seg = ((x + (ex - x) / ln * (r + 1.0), y + (ey - y) / ln * (r + 1.0)), (ex, ey))
                    slide = 0.6 if (fx, fy) != (fxs[0], fys[0]) else 0.0
                    out.append({"box": box, "seg": seg, "leader": seg is not None,
                                "cost": pref * 6 + slide + d * lin + quad * (d / 20.0) ** 2})
    return out


def _seg_box_hits(segs, boxes):
    """(K,) segments (None allowed) against (L,4) boxes -> (K,L) bool, sampled along each segment."""
    K, Lb = len(segs), len(boxes)
    out = np.zeros((K, Lb), dtype=bool)
    idx = [k for k, s in enumerate(segs) if s is not None]
    if not idx:
        return out
    S = np.array([segs[k] for k in idx])                  # (k,2,2)
    t = np.linspace(0.12, 0.88, 9)[None, :, None]
    P = S[:, None, 0, :] + (S[:, None, 1, :] - S[:, None, 0, :]) * t   # (k,9,2)
    B = np.asarray(boxes)
    inside = ((P[:, :, None, 0] > B[None, None, :, 0] - 1) & (P[:, :, None, 0] < B[None, None, :, 2] + 1) &
              (P[:, :, None, 1] > B[None, None, :, 1] - 1) & (P[:, :, None, 1] < B[None, None, :, 3] + 1))
    out[idx] = inside.any(axis=1)
    return out


def _seg_seg_cross(sa, sb):
    """Proper crossings between two lists of segments (None allowed) -> (Ka,Kb) bool."""
    out = np.zeros((len(sa), len(sb)), dtype=bool)
    ia = [k for k, s in enumerate(sa) if s is not None]
    ib = [k for k, s in enumerate(sb) if s is not None]
    if not ia or not ib:
        return out
    A = np.array([sa[k] for k in ia])[:, None]   # (a,1,2,2)
    B = np.array([sb[k] for k in ib])[None, :]   # (1,b,2,2)

    def orient(p, q, r):
        return (q[..., 0] - p[..., 0]) * (r[..., 1] - p[..., 1]) - (q[..., 1] - p[..., 1]) * (r[..., 0] - p[..., 0])
    p1, q1, p2, q2 = A[..., 0, :], A[..., 1, :], B[..., 0, :], B[..., 1, :]
    hit = ((orient(p1, q1, p2) * orient(p1, q1, q2) < 0) & (orient(p2, q2, p1) * orient(p2, q2, q1) < 0))
    out[np.ix_(ia, ib)] = hit
    return out


def _seg_near_point(seg, cx, cy, r):
    (x0, y0), (x1, y1) = seg
    dx, dy = x1 - x0, y1 - y0
    ln2 = dx * dx + dy * dy or 1.0
    t = max(0.0, min(1.0, ((cx - x0) * dx + (cy - y0) * dy) / ln2))
    return math.hypot(x0 + t * dx - cx, y0 + t * dy - cy) < r


def place_labels_compact(pts, widths, label_h, bounds, reserved, field, L):
    names = list(pts)
    N = len(names)
    r = L["dot_r"]
    W_, H_ = bounds
    cands = [fan_candidates(*pts[n], widths[n], label_h, L) for n in names]

    def box_dist(b, x, y):
        return math.hypot(x - min(max(x, b[0]), b[2]), y - min(max(y, b[1]), b[3]))

    def unary(i, c):
        cost = c["cost"]
        b = c["box"]
        if b[0] < 4 or b[1] < 4 or b[2] > W_ - 4 or b[3] > H_ - 4:
            cost += 400
        for rb in reserved:
            cost += overlap(b, rb, 2) * 2
        own = box_dist(b, *pts[names[i]])
        for j, m in enumerate(names):
            if box_hits_circle(b, *pts[m], r):
                cost += 160
            if j == i:
                continue
            dm = box_dist(b, *pts[m])
            if dm < 12:                       # keep some air between a label and other villages' dots
                cost += (12 - dm) * 3
            if not c["seg"] and dm < own + 3:  # a label must read as belonging to its own dot
                cost += 40
        x0, y0, x1, y1 = b[0] - 3, b[1] - 3, b[2] + 3, b[3] + 3
        xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
        ring = ((x0, y0), (xm, y0), (x1, y0), (x1, ym), (x1, y1), (xm, y1), (x0, y1), (x0, ym))
        cost += L["zone_w"] * sum(1 for sx, sy in ring if field(sx, sy) < ZONE_LEVEL)
        if c["seg"]:
            for j, m in enumerate(names):
                if j == i:
                    continue
                if _seg_near_point(c["seg"], *pts[m], r + 2.5):
                    cost += 120
                elif _seg_near_point(c["seg"], *pts[m], 12):   # leaders also keep clear of other dots
                    cost += 10
        return cost

    U = [np.array([unary(i, c) for c in cands[i]]) for i in range(N)]
    boxes = [np.array([c["box"] for c in cands[i]]) for i in range(N)]
    segs = [[c["seg"] for c in cands[i]] for i in range(N)]
    pad_x, pad_y = L["overlap_pad"]

    P = {}
    for i in range(N):
        for j in range(i + 1, N):
            A, B = boxes[i], boxes[j]
            ix = np.minimum(A[:, None, 2], B[None, :, 2]) - np.maximum(A[:, None, 0], B[None, :, 0]) + 2 * pad_x
            iy = np.minimum(A[:, None, 3], B[None, :, 3]) - np.maximum(A[:, None, 1], B[None, :, 1]) + 2 * pad_y
            M = np.clip(ix, 0, None) * np.clip(iy, 0, None) * 3
            M = M + 60 * _seg_box_hits(segs[i], B) + 60 * _seg_box_hits(segs[j], A).T
            M = M + 60 * _seg_seg_cross(segs[i], segs[j])
            if M.any():
                P[(i, j)] = M.tolist()
                P[(j, i)] = M.T.tolist()
    nbrs = [[j for j in range(N) if (i, j) in P] for i in range(N)]
    Ul = [u.tolist() for u in U]

    def total(ch):
        t = sum(Ul[i][ch[i]] for i in range(N))
        for (i, j), M in P.items():
            if i < j:
                t += M[ch[i]][ch[j]]
        return t

    best_all, best_all_cost = None, float("inf")
    for seed in L["seeds"]:
        rng = random.Random(seed)
        choice = [int(np.argmin(U[i])) for i in range(N)]
        cur = total(choice)
        best, best_cost = list(choice), cur
        temp = 60.0
        steps = L["steps"]
        decay = (0.05 / temp) ** (1 / steps)
        for _ in range(steps):
            i = rng.randrange(N)
            old = choice[i]
            new = rng.randrange(len(cands[i]))
            if new == old:
                temp *= decay
                continue
            u = Ul[i]
            delta = u[new] - u[old]
            for j in nbrs[i]:
                row = P[(i, j)]
                cj = choice[j]
                delta += row[new][cj] - row[old][cj]
            if delta <= 0 or rng.random() < math.exp(-delta / max(temp, 0.01)):
                choice[i] = new
                cur += delta
                if cur < best_cost - 1e-9:
                    best, best_cost = list(choice), cur
            temp *= decay
        if best_cost < best_all_cost:
            best_all, best_all_cost = best, best_cost
    return {n: cands[i][best_all[i]] for i, n in enumerate(names)}, total(best_all)


# ------------------------------------------------------------------ SVG
def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;")


def build(villages, layout="wide"):
    """villages: list of (latin name, arabic name). Returns (svg, info)."""
    L = LAYOUTS[layout]
    compact = layout == "compact"
    Wl, r = L["W"], L["dot_r"]
    ar_of = dict(villages)
    pts, s, h = project(L)
    names = [n for n, _ in villages if n in pts]
    missing = [n for n, _ in villages if n not in pts]

    contours, zone = terrain_and_zone(pts, s, h, L)

    # map furniture (reserved so labels avoid it)
    scale_km = 2
    sb_w = scale_km * s
    edge_y = L.get("edge_y", (BEIRUT_Y, BEKAA_Y))
    by = h * edge_y[0]    # edge arrows: Beirut on the west side, the Bekaa on the east
    ky_ = h * edge_y[1]
    if compact:
        sb_x, sb_y = 12.0, h - 11.0
        lx, ly = Wl - 100, h - 13
        reserved = [
            (Wl - 26, 4, Wl - 4, 36),                               # north arrow
            (4, by - 9, 58, by + 9),                                # Beirut
            (Wl - 58, ky_ - 9, Wl - 4, ky_ + 9),                    # Bekaa
            (lx - 4, ly - 9, Wl - 4, ly + 8),                       # legend
        ]
    else:
        sb_x, sb_y = 34.0, h - 40.0
        lx, ly = Wl - 222, h - 37
        reserved = [
            (sb_x - 6, sb_y - 26, sb_x + sb_w + 50, sb_y + 14),       # scale bar
            (Wl - 66, 18, Wl - 18, 84),                                  # north arrow
            (14, by - 22, 112, by + 22),                               # Beirut
            (Wl - 108, ky_ - 22, Wl - 14, ky_ + 22),                     # Bekaa
            (Wl - 230, h - 56, Wl - 18, h - 18),                          # legend
        ]
    # label_widths.json holds widths measured in the page fonts; a village that isn't in it
    # yet gets a generous estimate so its label still can't collide with its neighbours
    f_en, f_ar = L["font"][0] / FONT_EN, L["font"][1] / FONT_AR
    en_w = {n: (WIDTHS[n][0] if n in WIDTHS else len(n) * 10.5) * f_en for n in names}
    ar_w = {n: (WIDTHS[n][1] if n in WIDTHS else len(ar_of[n]) * 9.0) * f_ar for n in names}
    lh_en, lh_ar = L["label_h"]
    field = zone_field({n: pts[n] for n in names}, s)
    sub = {n: pts[n] for n in names}
    if compact:
        en_place, en_cost = place_labels_compact(sub, en_w, lh_en, (Wl, h), reserved, field, L)
        ar_place, ar_cost = place_labels_compact(sub, ar_w, lh_ar, (Wl, h), reserved, field, L)
    else:
        en_place, en_cost = place_labels(sub, en_w, lh_en, (Wl, h), reserved, field)
        ar_place, ar_cost = place_labels(sub, ar_w, lh_ar, (Wl, h), reserved, field, seed=5)

    # Hammana-outward order for the reveal ripple
    hx, hy = pts.get("Hammana", (Wl / 2, h / 2))
    order = sorted(names, key=lambda n: math.hypot(pts[n][0] - hx, pts[n][1] - hy))
    delay = {n: i * 70 for i, n in enumerate(order)}

    def label_svg(n, place, lang, lh):
        b = place["box"]
        x, y = pts[n]
        parts = []
        if place["leader"]:
            ex, ey = leader_end(b, x, y)
            ln = math.hypot(ex - x, ey - y) or 1.0
            sx, sy = x + (ex - x) / ln * (r + 1.0), y + (ey - y) / ln * (r + 1.0)
            parts.append(f'<path class="map-leader" d="M{sx:.1f} {sy:.1f}L{ex:.1f} {ey:.1f}"/>')
        text = n if lang == "en" else ar_of[n]
        base = b[1] + lh * (0.74 if lang == "en" else 0.72)
        parts.append(f'<text class="map-label" x="{b[0]:.1f}" y="{base:.1f}">{esc(text)}</text>')
        return "".join(parts)

    contour_svg = []
    idx_mod, idx_base = L["index"]
    for lvl, seg in contours:
        cls = "map-contour is-index" if (lvl - idx_base) % idx_mod == 0 else "map-contour"
        contour_svg.append(f'<path class="{cls}" d="{path_d(seg)}"/>')

    zone_svg = "".join(f'<path class="map-zone" d="{path_d(seg, closed=True)}"/>' for seg in zone)
    zone_line = "".join(f'<path class="map-zone-line" d="{path_d(seg, closed=True)}"/>' for seg in zone)

    hit_r = 10 if compact else 16
    villages_svg = []
    for n in names:
        x, y = pts[n]
        villages_svg.append(
            f'<g class="map-v" style="--d:{delay[n]}ms">'
            f'<circle class="map-ring" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>'
            f'<circle class="map-dot" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>'
            f'<g class="map-en">{label_svg(n, en_place[n], "en", lh_en)}</g>'
            f'<g class="map-ar" lang="ar">{label_svg(n, ar_place[n], "ar", lh_ar)}</g>'
            f'<circle class="map-hit" cx="{x:.1f}" cy="{y:.1f}" r="{hit_r}"/>'
            f'</g>')

    if compact:
        scale_svg = ""
        north = (f'<g class="map-north" transform="translate({Wl - 15:.1f} 9)">'
                 f'<path class="map-north-a" d="M0 0 L6 17 L0 13 Z"/><path class="map-north-b" d="M0 0 L-6 17 L0 13 Z"/>'
                 f'<text class="map-small map-n" x="0" y="28" text-anchor="middle">N</text></g>')
        edges = (f'<g class="map-edge">'
                 f'<path class="map-arrow" d="M8 {by:.1f} h16 M8 {by:.1f} l6 -4 M8 {by:.1f} l6 4"/>'
                 f'<text class="map-small map-en" x="29" y="{by + 3:.1f}">Beirut</text>'
                 f'<text class="map-small map-ar" lang="ar" x="29" y="{by + 3.5:.1f}">بيروت</text>'
                 f'<path class="map-arrow" d="M{Wl - 8:.1f} {ky_:.1f} h-16 M{Wl - 8:.1f} {ky_:.1f} l-6 -4 M{Wl - 8:.1f} {ky_:.1f} l-6 4"/>'
                 f'<text class="map-small map-en" x="{Wl - 29:.1f}" y="{ky_ + 3:.1f}" text-anchor="end">Bekaa</text>'
                 f'<text class="map-small map-ar" lang="ar" x="{Wl - 29:.1f}" y="{ky_ + 3.5:.1f}" text-anchor="end">البقاع</text>'
                 f'</g>')
        legend = (f'<g class="map-legend">'
                  f'<path class="map-zone-line" d="M{lx:.1f} {ly:.1f} h20"/>'
                  f'<text class="map-small map-en" x="{lx + 27:.1f}" y="{ly + 3:.1f}">Delivery area</text>'
                  f'<text class="map-small map-ar" lang="ar" x="{lx + 27:.1f}" y="{ly + 3.5:.1f}">منطقة التوصيل</text>'
                  f'</g>')
        pin = '<svg x="-7" y="-18" width="14" height="18" viewBox="0 0 181 231" overflow="visible">'
    else:
        ticks = "".join(
            f'<rect class="{"map-sb-a" if i % 2 == 0 else "map-sb-b"}" x="{sb_x + i * s:.1f}" y="{sb_y - 5:.1f}" width="{s:.1f}" height="6"/>'
            for i in range(scale_km))
        scale_svg = (f'<g class="map-scale">{ticks}'
                     f'<text class="map-small" x="{sb_x:.1f}" y="{sb_y - 12:.1f}">0</text>'
                     f'<text class="map-small map-en" x="{sb_x + sb_w + 8:.1f}" y="{sb_y + 1:.1f}">{scale_km} km</text>'
                     f'<text class="map-small map-ar" lang="ar" x="{sb_x + sb_w + 8:.1f}" y="{sb_y + 2:.1f}">{scale_km} كلم</text></g>')
        north = (f'<g class="map-north" transform="translate({Wl - 42:.1f} 30)">'
                 f'<path class="map-north-a" d="M0 0 L9 26 L0 20 Z"/><path class="map-north-b" d="M0 0 L-9 26 L0 20 Z"/>'
                 f'<text class="map-small map-n" x="0" y="44" text-anchor="middle">N</text></g>')
        edges = (f'<g class="map-edge">'
                 f'<path class="map-arrow" d="M22 {by:.1f} h26 M22 {by:.1f} l9 -6 M22 {by:.1f} l9 6"/>'
                 f'<text class="map-small map-en" x="56" y="{by + 4.5:.1f}">Beirut</text>'
                 f'<text class="map-small map-ar" lang="ar" x="56" y="{by + 5:.1f}">بيروت</text>'
                 f'<path class="map-arrow" d="M{Wl - 22:.1f} {ky_:.1f} h-26 M{Wl - 22:.1f} {ky_:.1f} l-9 -6 M{Wl - 22:.1f} {ky_:.1f} l-9 6"/>'
                 f'<text class="map-small map-en" x="{Wl - 56:.1f}" y="{ky_ + 4.5:.1f}" text-anchor="end">Bekaa</text>'
                 f'<text class="map-small map-ar" lang="ar" x="{Wl - 56:.1f}" y="{ky_ + 5:.1f}" text-anchor="end">البقاع</text>'
                 f'</g>')
        legend = (f'<g class="map-legend">'
                  f'<path class="map-zone-line" d="M{lx:.1f} {ly:.1f} h34"/>'
                  f'<text class="map-small map-en" x="{lx + 44:.1f}" y="{ly + 4.5:.1f}">Delivery area</text>'
                  f'<text class="map-small map-ar" lang="ar" x="{lx + 44:.1f}" y="{ly + 5:.1f}">منطقة التوصيل</text>'
                  f'</g>')
        pin = '<svg x="-9" y="-23" width="18" height="23" viewBox="0 0 181 231" overflow="visible">'

    names_list = ", ".join(n for n, _ in villages)
    title_id = f"mapTitle-{layout}"
    svg = (f'<svg class="village-map is-{layout}" viewBox="0 0 {Wl:.0f} {h:.0f}" role="img" aria-labelledby="{title_id}" focusable="false">'
           f'<title id="{title_id}">Map of the villages Jeetak delivers to in the Upper Metn: {esc(names_list)}</title>'
           f'<rect class="map-bg" width="{Wl:.0f}" height="{h:.0f}" rx="0"/>'
           f'<g class="map-contours">{"".join(contour_svg)}</g>'
           f'{zone_svg}{zone_line}'
           f'{edges}{north}{scale_svg}{legend}'
           f'<g class="map-villages">{"".join(villages_svg)}</g>'
           f'<g class="map-drop" transform="translate(-100 -100)"><g class="map-drop-pin">'
           f'{pin}'
           f'<circle class="pin-core" cx="90.5" cy="90.2" r="44"/><use href="#jk-pin" class="pin-fill"/></svg></g></g>'
           f'</svg>')
    info = {"width": Wl, "height": h, "hammana_x": hx / Wl, "missing": missing,
            "label_cost": [round(en_cost, 1), round(ar_cost, 1)], "km": s,
            "leaders": [sum(1 for p in en_place.values() if p["leader"]), sum(1 for p in ar_place.values() if p["leader"])]}
    return svg, info


def load_villages():
    src = (ROOT / "build.py").read_text()
    a = src.index("VILLAGES = [")
    b = src.index("]", src.index('("Saoufar", "صوفر")')) + 1
    ns = {}
    exec(src[a:b], ns)
    return ns["VILLAGES"]


if __name__ == "__main__":
    import sys
    import time
    layout = sys.argv[1] if len(sys.argv) > 1 else "wide"
    t0 = time.time()
    svg, info = build(load_villages(), layout)
    (ROOT / "out" / f"map-{layout}.svg").write_text(svg)
    print(info, len(svg), "bytes", f"{time.time() - t0:.1f}s")
