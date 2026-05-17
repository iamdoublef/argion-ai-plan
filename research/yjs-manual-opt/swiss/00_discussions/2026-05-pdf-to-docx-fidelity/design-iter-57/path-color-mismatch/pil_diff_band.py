"""Find horizontal diff bands on p3 between target and candidate.

Compute row-by-row average diff to spot where the geometric/textual mismatch
is concentrated.
"""
from PIL import Image
import numpy as np
from pathlib import Path
import sys

TARGET = Path("D:/work/private/yjsplan/research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/baseline/target_png")
CAND_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("D:/work/private/yjsplan/research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/design-iter-57/path-color-mismatch/iter-3n/_score_tmp/png")

page = sys.argv[2] if len(sys.argv) > 2 else "03"
tgt = np.array(Image.open(TARGET / f"page-{page}.png").convert("RGB"))
cand = np.array(Image.open(CAND_DIR / f"page-{page}.png").convert("RGB"))

# Resize if needed
if tgt.shape != cand.shape:
    print(f"shape mismatch: tgt={tgt.shape} cand={cand.shape}")
    from PIL import Image as PILImage
    cand_img = PILImage.fromarray(cand)
    cand_img = cand_img.resize((tgt.shape[1], tgt.shape[0]))
    cand = np.array(cand_img)

diff = np.abs(tgt.astype(int) - cand.astype(int))
# Mean per row
row_diff = diff.mean(axis=(1, 2))
H = len(row_diff)

# Print biggest 20 rows
top_idx = np.argsort(-row_diff)[:25]
print(f"page {page}: total mean diff = {diff.mean():.2f}")
print("top-25 rows with biggest diff:")
for i in sorted(top_idx):
    print(f"  row {i} (y_frac={i/H:.3f}): diff={row_diff[i]:.1f}")

# bucket into 10% bands and show
print("\n10% bands (mean diff):")
band_size = H // 10
for b in range(10):
    s, e = b*band_size, (b+1)*band_size
    print(f"  y={b*10}-{(b+1)*10}% (rows {s}-{e}): {row_diff[s:e].mean():.2f}")
