"""iter-1: visual diff analysis between target p14 and candidate p14.

Generates:
- diff.png: red overlay where diffs exist
- bands.json: per-Y-band diff sum (find horizontal hotspots)
- hotspots.txt: report
"""
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).parent
# ROOT.parents: [0] path-p14-structural, [1] design-iter-54, [2] 2026-05-pdf-to-docx-fidelity
DISC = ROOT.parents[1]
TARGET = DISC / "baseline" / "target_png" / "page-14.png"
CANDIDATE = DISC / "final" / "_score_tmp" / "png" / "page-14.png"

OUT = ROOT / "iter-1"
OUT.mkdir(exist_ok=True)


def diff_analysis():
    t = Image.open(TARGET).convert("RGB")
    c = Image.open(CANDIDATE).convert("RGB")
    print(f"target size {t.size} candidate size {c.size}")
    if t.size != c.size:
        # resize candidate to target
        c = c.resize(t.size)
    d = ImageChops.difference(t, c)
    diff_gray = d.convert("L")
    # per row band sum
    w, h = t.size
    rows = []
    px = diff_gray.load()
    for y in range(h):
        s = 0
        for x in range(w):
            s += px[x, y]
        rows.append(s)
    # Total row sum normalized
    max_row = max(rows)
    # Find hot bands: y where row_sum > 0.3 * max_row
    threshold = 0.3 * max_row
    hot_bands = []
    in_band = False
    start = 0
    for y, s in enumerate(rows):
        if s > threshold and not in_band:
            start = y
            in_band = True
        elif s <= threshold and in_band:
            hot_bands.append((start, y - 1, sum(rows[start:y])))
            in_band = False
    if in_band:
        hot_bands.append((start, h - 1, sum(rows[start:h])))

    # Save band data
    (OUT / "rows.json").write_text(json.dumps(rows), encoding="utf-8")
    (OUT / "hot_bands.json").write_text(json.dumps(hot_bands), encoding="utf-8")

    # Save annotated diff image
    annotated = t.copy()
    drw = ImageDraw.Draw(annotated, "RGBA")
    for y0, y1, s in hot_bands:
        drw.rectangle([0, y0, w - 1, y1], outline=(255, 0, 0, 255), width=2)
    annotated.save(OUT / "annotated.png")

    # Save raw diff
    d.save(OUT / "diff.png")
    diff_gray.save(OUT / "diff_gray.png")

    print(f"image size: {w}x{h}")
    print(f"total diff: {sum(rows)}")
    print(f"max row diff: {max_row}")
    print(f"hot bands (threshold {threshold:.0f}):")
    for y0, y1, s in hot_bands:
        print(f"  y={y0:>4}..{y1:>4} sum={s:>10}  (rel-y {y0/h:.2%}..{y1/h:.2%})")

    return hot_bands, w, h


def column_analysis(hot_bands, w, h):
    """For each hot band, find which X columns dominate diff."""
    t = Image.open(TARGET).convert("RGB")
    c = Image.open(CANDIDATE).convert("RGB")
    if t.size != c.size:
        c = c.resize(t.size)
    diff_gray = ImageChops.difference(t, c).convert("L")
    px = diff_gray.load()

    band_x_profiles = []
    for y0, y1, s in hot_bands:
        cols = [0] * w
        for y in range(y0, y1 + 1):
            for x in range(w):
                cols[x] += px[x, y]
        # Find X hot zones
        max_col = max(cols) if cols else 1
        threshold = 0.3 * max_col
        x_zones = []
        in_zone = False
        start = 0
        for x, v in enumerate(cols):
            if v > threshold and not in_zone:
                start = x
                in_zone = True
            elif v <= threshold and in_zone:
                x_zones.append((start, x - 1, sum(cols[start:x])))
                in_zone = False
        if in_zone:
            x_zones.append((start, w - 1, sum(cols[start:w])))
        band_x_profiles.append({
            "y_band": [y0, y1],
            "y_sum": s,
            "x_zones": x_zones,
        })
        print(f"\nBand y={y0}..{y1} (sum={s}):")
        for xs, xe, xv in x_zones:
            print(f"  x={xs:>4}..{xe:>4} sum={xv:>10}  ({xs/w:.2%}..{xe/w:.2%})")
    (OUT / "band_x_profiles.json").write_text(json.dumps(band_x_profiles), encoding="utf-8")


if __name__ == "__main__":
    bands, w, h = diff_analysis()
    column_analysis(bands, w, h)
