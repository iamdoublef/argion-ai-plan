"""Measure text height in target PDF p3 vs candidate render."""
from PIL import Image
import numpy as np
from pathlib import Path

# Sample p3 body — find a bullet line, measure its black-pixel vertical extent
TARGET = Path("D:/work/private/yjsplan/research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/baseline/target_png/page-03.png")

img = np.array(Image.open(TARGET).convert("L"))
H, W = img.shape
print(f"size: {W}x{H}")

# Body region — find dark rows in y=0.30..0.85
# For each row in body, count number of dark pixels (< 50)
y0, y1 = int(H*0.30), int(H*0.85)
x0, x1 = int(W*0.15), int(W*0.85)

dark_per_row = (img[y0:y1, x0:x1] < 80).sum(axis=1)
# Find groups of consecutive non-zero rows (text lines)
in_text = False
lines = []
start = 0
for i, c in enumerate(dark_per_row):
    if c >= 4 and not in_text:
        start = i
        in_text = True
    elif c < 4 and in_text:
        lines.append((y0+start, y0+i, y0+i - (y0+start)))
        in_text = False
if in_text:
    lines.append((y0+start, y0+len(dark_per_row), len(dark_per_row)-start))

# Show heights
heights = [h for _, _, h in lines]
import statistics
print(f"detected {len(lines)} text lines in body region")
print(f"line heights: {heights}")
print(f"median: {statistics.median(heights)}  mean: {statistics.mean(heights):.1f}")
