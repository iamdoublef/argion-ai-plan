"""Sample colors from target PNG and candidate baseline render.

Strategy:
- Open page-03.png from target_png/
- For known regions (banner, body text, gray text, red dots, headers),
  crop and compute the dominant non-white color.
- Compare to baseline candidate p3 if available.
"""
from PIL import Image
from collections import Counter
from pathlib import Path
import sys

TARGET_PNG_DIR = Path("D:/work/private/yjsplan/research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/baseline/target_png")
CAND_PNG_DIR = Path("D:/work/private/yjsplan/research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/baseline/current_docx_png")

def sample_region(img, box, label=""):
    """Crop and return Counter of colors, dropping near-white."""
    crop = img.crop(box).convert("RGB")
    pixels = list(crop.getdata())
    # Filter out near-white pixels
    non_white = [p for p in pixels if not (p[0] > 245 and p[1] > 245 and p[2] > 245)]
    if not non_white:
        return Counter()
    # Bucket to nearest 4-step for grouping similar
    bucketed = [(p[0]//8*8, p[1]//8*8, p[2]//8*8) for p in non_white]
    return Counter(bucketed)


def show_top(cnt, label, n=8):
    if not cnt:
        print(f"  {label}: NO non-white pixels")
        return
    total = sum(cnt.values())
    print(f"  {label}: top {n} of {total} non-white")
    for color, count in cnt.most_common(n):
        pct = 100.0 * count / total
        hex_c = f"{color[0]:02X}{color[1]:02X}{color[2]:02X}"
        print(f"    {color} = #{hex_c} ({pct:.1f}%)")


if __name__ == "__main__":
    page = sys.argv[1] if len(sys.argv) > 1 else "03"
    tgt = TARGET_PNG_DIR / f"page-{page}.png"
    cand = CAND_PNG_DIR / f"page-{page}.png" if CAND_PNG_DIR.exists() else None

    print(f"=== Page {page} TARGET ({tgt}) ===")
    img = Image.open(tgt)
    W, H = img.size
    print(f"size: {W}x{H}")

    # Page split into thirds vertically: header, body, footer
    # On p3, banner is at top, then warnings (24 bullets)

    # Banner stripe — top ~12% (header banner area)
    banner = sample_region(img, (0, int(H*0.04), W, int(H*0.15)), "banner top stripe")
    show_top(banner, "banner")

    # Title area — y around 0.10-0.18
    title = sample_region(img, (int(W*0.05), int(H*0.10), int(W*0.55), int(H*0.20)), "title region")
    show_top(title, "title")

    # Body text area — center
    body = sample_region(img, (int(W*0.15), int(H*0.25), int(W*0.85), int(H*0.75)), "body region")
    show_top(body, "body")

    # Red dots/icons region — left margin
    lhs = sample_region(img, (int(W*0.04), int(H*0.20), int(W*0.20), int(H*0.85)), "left margin region")
    show_top(lhs, "left margin")

    # Footer
    foot = sample_region(img, (0, int(H*0.90), W, H), "footer")
    show_top(foot, "footer")
