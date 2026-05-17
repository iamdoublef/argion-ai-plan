"""Side-by-side diff of target vs candidate for a single page."""
import sys
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).parent
TARGET_PNG = ROOT.parent.parent / "baseline" / "target_png"
CAND_PNG = ROOT / "iter-2" / "_score_tmp" / "png"


def diff_page(page_num: int):
    t = Image.open(TARGET_PNG / f"page-{page_num:02d}.png").convert("RGB")
    c = Image.open(CAND_PNG / f"page-{page_num:02d}.png").convert("RGB")
    if t.size != c.size:
        c = c.resize(t.size, Image.BICUBIC)
    d = ImageChops.difference(t, c)
    # Amplify diff
    pixels = d.load()
    for y in range(d.size[1]):
        for x in range(d.size[0]):
            r, g, b = pixels[x, y]
            mx = max(r, g, b)
            if mx > 5:
                pixels[x, y] = (min(255, r*8), min(255, g*8), min(255, b*8))

    # Side by side
    w = t.size[0]
    h = t.size[1]
    combo = Image.new("RGB", (w * 3 + 20, h), "white")
    combo.paste(t, (0, 0))
    combo.paste(c, (w + 10, 0))
    combo.paste(d, (w * 2 + 20, 0))

    out = ROOT / f"diff-page-{page_num:02d}.png"
    combo.save(out, optimize=True)
    print(f"Saved {out}")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        diff_page(int(p))
