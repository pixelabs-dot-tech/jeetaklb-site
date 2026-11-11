"""QR code for the desktop sign-off: opens jeetaklb.com on a phone. Writes revamp/assets/qr.json
({"size": modules per side, "d": one SVG path}) and checks that the drawn code reads back correctly."""
import json
from pathlib import Path
import segno

URL = "https://jeetaklb.com"
HERE = Path(__file__).resolve().parent.parent
qr = segno.make(URL, error="m", micro=False)
rows = [list(r) for r in qr.matrix]
n = len(rows)
d = []
for y, row in enumerate(rows):
    x = 0
    while x < n:
        if row[x]:
            x0 = x
            while x < n and row[x]:
                x += 1
            d.append(f"M{x0} {y}h{x - x0}v1h-{x - x0}z")
        else:
            x += 1
(HERE / "assets" / "qr.json").write_text(json.dumps({"url": URL, "size": n, "d": "".join(d)}))
print("version", qr.version, "error", qr.error, "modules", n, "path chars", len("".join(d)))

# read it back from a rendering, the way a phone camera would
import cv2
import numpy as np
scale, quiet = 8, 4
img = np.full(((n + 2 * quiet) * scale, (n + 2 * quiet) * scale), 255, np.uint8)
for y, row in enumerate(rows):
    for x, v in enumerate(row):
        if v:
            img[(y + quiet) * scale:(y + quiet + 1) * scale, (x + quiet) * scale:(x + quiet + 1) * scale] = 0
text, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
assert text == URL, repr(text)
print("reads back as", text)
