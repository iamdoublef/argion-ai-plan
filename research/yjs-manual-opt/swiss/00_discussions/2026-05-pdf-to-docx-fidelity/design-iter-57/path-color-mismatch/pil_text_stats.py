"""Compare text density and text-line counts between tgt and candidate."""
from PIL import Image
import numpy as np
from pathlib import Path

TARGET = Path("D:/work/private/yjsplan/research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/baseline/target_png/page-03.png")
CAND = Path("D:/work/private/yjsplan/research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/design-iter-57/path-color-mismatch/iter-3n/_score_tmp/png/page-03.png")

def detect_lines(path, label):
    img = np.array(Image.open(path).convert("L"))
    H, W = img.shape
    y0, y1 = int(H*0.25), int(H*0.75)
    x0, x1 = int(W*0.15), int(W*0.85)
    dark_per_row = (img[y0:y1, x0:x1] < 100).sum(axis=1)
    in_text = False
    lines = []
    start = 0
    for i, c in enumerate(dark_per_row):
        if c >= 4 and not in_text:
            start = i
            in_text = True
        elif c < 4 and in_text:
            lines.append((y0+start, y0+i, i - start))
            in_text = False
    heights = [h for _, _, h in lines]
    # space between lines
    spaces = []
    for i in range(1, len(lines)):
        spaces.append(lines[i][0] - lines[i-1][1])
    print(f"{label}: {len(lines)} lines, heights={heights[:10]}..., line-gaps={spaces[:10]}...")
    if heights:
        print(f"  median height: {sorted(heights)[len(heights)//2]}")
    if spaces:
        print(f"  median gap: {sorted(spaces)[len(spaces)//2]}")
    return lines

detect_lines(TARGET, "TARGET p3")
detect_lines(CAND, "CAND   p3")
