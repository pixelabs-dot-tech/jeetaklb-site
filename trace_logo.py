import json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
import potrace

SRC = str(Path(__file__).parent / 'logo-source.png')
a = np.array(Image.open(SRC).convert('RGB')).astype(int)
mask = a[:, :, 1] > 128
lab, n = ndimage.label(mask)

def group_mask(ids):
    return np.isin(lab, ids)

def trace(m, ox, oy):
    bm = potrace.Bitmap(~m)
    plist = bm.trace(turdsize=4, alphamax=1.0, opticurve=True, opttolerance=0.2)
    f = lambda v: f"{v:.1f}".rstrip('0').rstrip('.')
    parts = []
    for curve in plist:
        s = curve.start_point
        d = [f"M{f(s.x-ox)} {f(s.y-oy)}"]
        for seg in curve.segments:
            if seg.is_corner:
                d.append(f"L{f(seg.c.x-ox)} {f(seg.c.y-oy)}L{f(seg.end_point.x-ox)} {f(seg.end_point.y-oy)}")
            else:
                d.append(f"C{f(seg.c1.x-ox)} {f(seg.c1.y-oy)} {f(seg.c2.x-ox)} {f(seg.c2.y-oy)} {f(seg.end_point.x-ox)} {f(seg.end_point.y-oy)}")
        d.append('Z')
        parts.append(''.join(d))
    return ''.join(parts)

def bbox(m, pad=2):
    ys, xs = np.where(m)
    return xs.min()-pad, ys.min()-pad, xs.max()+1+pad, ys.max()+1+pad

out = {}
groups = {
    'wordmark': list(range(1, 8)),
    'slogan': list(range(8, 20)),
    'pin': [1],
}
# lockup origin shared so wordmark+slogan align
lock = group_mask(list(range(1, 20)))
lx0, ly0, lx1, ly1 = bbox(lock)
out['lockup_box'] = [int(lx1-lx0), int(ly1-ly0)]
for name, ids in groups.items():
    m = group_mask(ids)
    x0, y0, x1, y1 = bbox(m)
    if name in ('wordmark', 'slogan'):
        # keep lockup coordinates for these two
        out[name] = {'d': trace(m, lx0, ly0), 'box': [int(x0-lx0), int(y0-ly0), int(x1-x0), int(y1-y0)]}
    else:
        out[name] = {'d': trace(m, x0, y0), 'box': [0, 0, int(x1-x0), int(y1-y0)]}
json.dump(out, open('logo_paths.json', 'w'))
for k, v in out.items():
    if isinstance(v, dict):
        print(k, v['box'], len(v['d']), 'chars')
    else:
        print(k, v)
