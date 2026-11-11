"""Cut the delivery bag out of its white studio background (brand kit photo) -> transparent WebP."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

src, out = Path(sys.argv[1]), Path(sys.argv[2])
width = int(sys.argv[3]) if len(sys.argv) > 3 else 900
rgb = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
mn, mx = rgb.min(axis=2), rgb.max(axis=2)
sat = (mx - mn) / np.maximum(mx, 1)

# background: near-white regions that touch the frame, plus the gap inside the carry handle
lab, n = ndi.label(mn >= 246)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
sizes = ndi.sum(np.ones_like(lab), lab, range(1, n + 1))
gaps = {i + 1 for i, s in enumerate(sizes) if s > 1500} - border
bg = np.isin(lab, list(border | gaps))

# the soft contact shadow: pale, colourless pixels that the background reaches
pale = mn > 105            # lighter than any orange fabric or black strap can be
lab2, _ = ndi.label(pale | bg)
reach = np.isin(lab2, list(set(np.unique(lab2[bg])) - {0}))
shadow = reach & ~bg

solid = ~reach
core = ndi.binary_erosion(solid, iterations=2)
# colours: push the bag's own colours out over the anti-aliased fringe so no white halo survives
_, (iy, ix) = ndi.distance_transform_edt(~core, return_indices=True)
col = rgb[iy, ix]
alpha = ndi.gaussian_filter(ndi.binary_erosion(solid, iterations=1).astype(np.float32), 0.9)
alpha = np.clip(alpha * 1.15, 0, 1)

sh = np.where(shadow, (255 - rgb.mean(axis=2)) / 255.0, 0)
sh = ndi.gaussian_filter(sh, 1.2) * 0.9
out_a = np.clip(alpha + (1 - alpha) * sh, 0, 1)
w = np.where(out_a > 0, alpha / np.maximum(out_a, 1e-6), 1)[..., None]
out_rgb = col * w            # the shadow part is black

im = Image.fromarray(np.dstack([out_rgb, out_a[..., None] * 255]).clip(0, 255).astype(np.uint8), "RGBA")
box = im.getchannel("A").point(lambda v: 255 if v > 6 else 0).getbbox()
pad = 6
box = (max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad))
im = im.crop(box)
im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
im.save(out, "WEBP", quality=82, method=6)
print(out, im.size, out.stat().st_size, "bytes")
