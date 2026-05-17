"""Inspect the top horizontal bar / banner area in detail."""
from PIL import Image
import numpy as np
from pathlib import Path

TARGET = Path("D:/work/private/yjsplan/research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/baseline/target_png/page-03.png")
CAND = Path("D:/work/private/yjsplan/research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/design-iter-57/path-color-mismatch/iter-3n/_score_tmp/png/page-03.png")

tgt = np.array(Image.open(TARGET).convert("L"))
cand = np.array(Image.open(CAND).convert("L"))
# Resize cand to match
if cand.shape != tgt.shape:
    from PIL import Image as I
    cand = np.array(I.fromarray(cand).resize((tgt.shape[1], tgt.shape[0])))

# Row 59-60: how much black is on each row in tgt vs cand
for y in range(50, 80):
    tgt_dark = (tgt[y] < 80).sum()
    cand_dark = (cand[y] < 80).sum()
    if tgt_dark > 100 or cand_dark > 100:
        diff = abs(tgt_dark - cand_dark)
        print(f"y={y}: tgt black={tgt_dark:4d}  cand black={cand_dark:4d}  diff={diff}")
