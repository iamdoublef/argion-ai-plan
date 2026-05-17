"""Crop and save specific row to look at it visually."""
from PIL import Image
from pathlib import Path
import sys

TARGET = Path("D:/work/private/yjsplan/research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/baseline/target_png/page-03.png")
CAND = Path("D:/work/private/yjsplan/research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/design-iter-57/path-color-mismatch/iter-3n/_score_tmp/png/page-03.png")

y0 = int(sys.argv[1]) if len(sys.argv) > 1 else 860
y1 = int(sys.argv[2]) if len(sys.argv) > 2 else 890

tgt = Image.open(TARGET)
cand = Image.open(CAND)

# Crop and save
out_t = Path(f"/tmp/tgt_{y0}_{y1}.png")
out_c = Path(f"/tmp/cand_{y0}_{y1}.png")
out_t.parent.mkdir(exist_ok=True, parents=True)

tgt.crop((0, y0, tgt.width, y1)).save(str(out_t))
cand.crop((0, y0, cand.width, y1)).save(str(out_c))
print(f"Saved: {out_t}, {out_c}")
