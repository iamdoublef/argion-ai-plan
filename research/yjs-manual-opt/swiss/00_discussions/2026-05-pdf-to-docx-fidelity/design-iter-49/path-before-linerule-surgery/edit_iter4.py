"""iter-4: w:lineRule="auto" -> "exact" globally.
292 sites currently use auto. Switch all to exact.
NOTE: With lineRule=exact, w:line value is interpreted in twips (1/20 of a point)
absolutely. With auto, line value is a multiplier *240 = 1.0 line.
Current line=240 with auto = single spacing. With exact, line=240 twips = 12pt fixed.
This is a structurally different rendering — could shrink lines significantly.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
doc_path = ROOT / "iter-4" / "unpacked" / "word" / "document.xml"
doc = doc_path.read_text(encoding="utf-8")

before = len(re.findall(r'w:lineRule="auto"', doc))
doc2 = re.sub(r'w:lineRule="auto"', 'w:lineRule="exact"', doc)
after = len(re.findall(r'w:lineRule="exact"', doc2))
print(f"auto sites pre: {before}, exact sites post: {after}")

doc_path.write_text(doc2, encoding="utf-8")
