"""Check fonts used in a PDF."""
import sys
import fitz
from pathlib import Path
from collections import Counter

p = Path(sys.argv[1])
d = fitz.open(p)
fonts = Counter()
sizes = Counter()
for page in d:
    td = page.get_text("dict")
    for block in td.get("blocks", []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                fonts[span.get("font", "?")] += 1
                sizes[round(span.get("size", 0), 1)] += 1
d.close()
print("FONTS:")
for f, n in fonts.most_common():
    print(f"  {n:5d}  {f}")
print("SIZES:")
for s, n in sizes.most_common(15):
    print(f"  {n:5d}  {s}pt")
