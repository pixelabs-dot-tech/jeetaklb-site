"""The coverage map for the redesign: the same drawing code as the live site (village_map.py),
with the labels measured in Cairo (revamp/label_widths.json). Cached in revamp/map_cache.json."""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))


def villages():
    src = (ROOT / "build.py").read_text()
    a = src.index("VILLAGES = [")
    b = src.index("]", src.index('("Saoufar", "صوفر")')) + 1
    ns = {}
    exec(src[a:b], ns)
    return ns["VILLAGES"]


def maps():
    """Returns {"wide": {"svg", "info"}, "compact": {...}}; redraws (about 90 seconds) only when an input changed."""
    vs = villages()
    widths_src = (HERE / "label_widths.json").read_text()
    key_src = "".join((ROOT / f).read_text() for f in ("village_map.py", "village_coords.py")) + widths_src
    key = hashlib.sha256((key_src + repr(vs)).encode()).hexdigest()[:16]
    cache = HERE / "map_cache.json"
    data = json.loads(cache.read_text()) if cache.exists() else {}
    if data.get("key") != key:
        import village_map   # needs matplotlib
        village_map.WIDTHS = json.loads(widths_src)
        data = {"key": key}
        for layout in ("wide", "compact"):
            svg, info = village_map.build(vs, layout)
            data[layout] = {"svg": svg, "info": info}
        cache.write_text(json.dumps(data, ensure_ascii=False))
    return data


if __name__ == "__main__":
    d = maps()
    for layout in ("wide", "compact"):
        print(layout, d[layout]["info"])
