"""Compare target vs candidate at specific rows to identify mismatch type."""
from PIL import Image
import numpy as np
from pathlib import Path
import sys

TARGET = Path("D:/work/private/yjsplan/research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/baseline/target_png")
CAND_DIR = Path("D:/work/private/yjsplan/research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/design-iter-57/path-color-mismatch/iter-3n/_score_tmp/png")

page = "03"
tgt = Image.open(TARGET / f"page-{page}.png").convert("RGB")
cand = Image.open(CAND_DIR / f"page-{page}.png").convert("RGB")
# Resize cand to match
cand = cand.resize(tgt.size)

# Specific bands of interest
bands = [
    ("banner-stripe-row-50-75", 50, 75),
    ("title-row-160-200", 160, 200),
    ("body-bullets-row-300-700", 300, 700),
    ("bottom-row-820-880", 820, 880),
]

for label, y0, y1 in bands:
    tgt_band = np.array(tgt.crop((0, y0, tgt.width, y1)))
    cand_band = np.array(cand.crop((0, y0, cand.width, y1)))

    # Statistics per region
    # Show black/red/white split
    is_black = (tgt_band.sum(axis=2) < 100)
    is_red = ((tgt_band[:,:,0] > 150) & (tgt_band[:,:,1] < 100) & (tgt_band[:,:,2] < 100))
    is_white = (tgt_band.sum(axis=2) > 720)
    cand_is_black = (cand_band.sum(axis=2) < 100)
    cand_is_red = ((cand_band[:,:,0] > 150) & (cand_band[:,:,1] < 100) & (cand_band[:,:,2] < 100))
    cand_is_white = (cand_band.sum(axis=2) > 720)
    total = tgt_band.shape[0] * tgt_band.shape[1]
    print(f"=== {label} ===")
    print(f"  TGT:  black={is_black.sum()/total*100:.1f}% red={is_red.sum()/total*100:.1f}% white={is_white.sum()/total*100:.1f}%")
    print(f"  CAND: black={cand_is_black.sum()/total*100:.1f}% red={cand_is_red.sum()/total*100:.1f}% white={cand_is_white.sum()/total*100:.1f}%")

    # Diff
    diff = np.abs(tgt_band.astype(int) - cand_band.astype(int))
    print(f"  diff mean: {diff.mean():.1f}")
